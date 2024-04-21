use std::{collections::HashMap, sync::Arc};

use mysql_async::{prelude::Queryable, Pool};
use axum::{
    extract::State, response::IntoResponse, routing::{get, post}, Json, Router
};
use serde::Deserialize;
use sha1::{Digest, Sha1};
use tokio::sync::{Mutex, RwLock};

#[derive(Clone)]
struct User {
    lock: Arc<Mutex<()>>,
    secret: u32
}

impl User {
    fn new() -> User {
        User {
            lock: Arc::new(Mutex::new(())),
            secret: rand::random::<u32>()
        }
    }
}

#[derive(Clone)]
struct AppState {
    users: Arc<RwLock<HashMap<u64, User>>>,
    pool: Arc<Pool>
}

impl AppState {
    fn new(pool: Pool) -> AppState {
        AppState { 
            users: Arc::new(RwLock::new(HashMap::new())),
            pool: Arc::new(pool)
        }
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let url = "mysql://fearless_concurrency:fearless_concurrency@database:3306/fearless_concurrency";

    let pool = Pool::new(url);

    let mut conn = pool.get_conn().await.unwrap();
    conn.exec_drop("CREATE TABLE IF NOT EXISTS info (body varchar(255))", ()).await.unwrap();
    conn.exec_drop("INSERT INTO info VALUES ('Hello, world')", ()).await.unwrap();

    let state = AppState::new(pool);
    let app = Router::new()
        .route("/", get(root))
        .route("/register", post(register))
        .route("/query", post(query))
        .route("/flag", post(flag))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("Listener started on port 3000");
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, World!"
}

async fn register(State(state): State<AppState>) -> impl IntoResponse {
    let uid = rand::random::<u64>();
    let mut users = state.users.write().await;
    let user = User::new();
    users.insert(uid, user);
    uid.to_string()
}

#[derive(Deserialize)]
struct Query {
    user_id: u64,
    query_string: String
}

async fn query(State(state): State<AppState>, Json(body): Json<Query>) -> axum::response::Result<String> {
    let users = state.users.read().await;
    let user = users.get(&body.user_id).ok_or_else(|| "User not found! Register first!")?;
    let user = user.clone();

    // Prevent registrations from being blocked while query is running
    // Fearless concurrency :tm:
    drop(users);

    // Prevent concurrent access to the database!
    // Don't even try any race condition thingies
    // They don't exist in rust!
    let _lock = user.lock.lock().await;
    let mut conn = state.pool.get_conn().await.map_err(|_| "Failed to acquire connection")?;

    // Unguessable table name (requires knowledge of user id and random table id)
    let table_id = rand::random::<u32>();
    let mut hasher = Sha1::new();
    hasher.update(b"fearless_concurrency");
    hasher.update(body.user_id.to_le_bytes());
    let table_name = format!("tbl_{}_{}", hex::encode(hasher.finalize()), table_id);

    let table_name = dbg!(table_name);
    let qs = dbg!(body.query_string);

    // Create temporary, unguessable table to store user secret
    conn.exec_drop(
        format!("CREATE TABLE {} (secret int unsigned)", table_name), ()
    ).await.map_err(|_| "Failed to create table")?;

    conn.exec_drop(
        format!("INSERT INTO {} values ({})", table_name, user.secret), ()
    ).await.map_err(|_| "Failed to insert secret")?;


    // Secret can't be leaked here since table name is unguessable!
    let res = conn.exec_first::<String, _, _>(
        format!("SELECT * FROM info WHERE body LIKE '{}'", qs),
        ()
    ).await;

    // You'll never get the secret!
    conn.exec_drop(
        format!("DROP TABLE {}", table_name), ()
    ).await.map_err(|_| "Failed to drop table")?;

    let res = res.map_err(|_| "Failed to run query")?;

    // _lock is automatically dropped when function exits, releasing the user lock

    if let Some(result) = res {
        return Ok(result);
    }
    Ok(String::from("No results!"))
}


#[derive(Deserialize)]
struct ClaimFlag {
    user_id: u64,
    secret: u32
}

async fn flag(State(state): State<AppState>, Json(body): Json<ClaimFlag>)  -> axum::response::Result<String> {
    let users = state.users.read().await;
    let user = users.get(&body.user_id).ok_or_else(|| "User not found! Register first!")?;

    if user.secret == body.secret {
        return Ok(String::from("grey{fake_flag_for_testing}"));
    }
    Ok(String::from("Wrong!"))
}