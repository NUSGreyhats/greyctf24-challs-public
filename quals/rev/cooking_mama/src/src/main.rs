use std::io;
use std::io::Write;

fn main() {
    cook();
    let mut board = [[0i32; 9]; 9];
    board = [[0, 5, 0, 0, 0, 0, 0, 8, 9],
 [7, 0, 0, 6, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 8, 4, 0, 0],
 [0, 0, 0, 0, 0, 1, 0, 9, 7],
 [0, 0, 0, 0, 3, 6, 2, 0, 0],
 [2, 0, 4, 0, 0, 0, 0, 0, 5],
 [6, 4, 2, 1, 0, 0, 0, 0, 0],
 [0, 0, 1, 8, 9, 0, 0, 0, 0],
 [0, 0, 8, 0, 6, 0, 5, 3, 0]];

    let mut input_string = String::new();
    print!("> ");
    io::stdout().flush().unwrap();
    
    io::stdin().read_line(&mut input_string).unwrap();

    for i in input_string.chars() {
        let num: i32 = i as i32 - '0' as i32;
        if num > 0 && num < 10 {
            welp(num, &mut board);
        }
    }

    if check_horizontal(&board) && check_vertical(&board) && check_square(&board) {
        cooked();
    } else {
        cook_harder();
    }
}

fn welp(num: i32, board: &mut [[i32; 9]; 9]) {
    for j in 0..9 {
        for k in 0..9 {
            if board[j][k] == 0 {
                board[j][k] = num;
                return
            }
        }
    }
}

fn check_horizontal(input: &[[i32; 9]; 9]) -> bool {
    let mut exists = [0i32; 9];
    let mut n = 0;

    while n < 9 {
        for i in 0..9 {
            let num = input[n][i];
            if num == 0 {
                return false;
            }
            exists[num as usize - 1] = 1;
        }

        n += 1;
    
        for i in exists {
            if i != 1 {
                return false;
            }
        }

        for j in exists.iter_mut() { *j = 0; }
    }
    true
}

fn check_vertical(input: &[[i32; 9]; 9]) -> bool {
    let mut exists = [0i32; 9];
    let mut n = 0;

    while n < 9 {
        for i in 0..9 {
            let num = input[i][n];
            if num == 0 {
                return false;
            }

            exists[num as usize - 1] = 1;
        }

        n += 1;
    
        for i in exists {
            if i != 1 {
                return false;
            }
        }

        for j in exists.iter_mut() { *j = 0; }
    }
    true
}

fn check_square(input: &[[i32; 9]; 9]) -> bool { 
    let mut exists = [0i32; 9]; 
    let mut flat = [0i32; 81]; 
 
    for i in 0..9 { 
        for j in 0..9 { 
            flat[i*9 + j] = input[i][j]; 
        } 
    } 
 
    for i in 0..9 { 
        let start = 27* (i / 3) + (i % 3) * 3; 
        for j in 0..9 { 
            let num = flat[start + (j % 3) + (9 * (j / 3))]; 
            if num == 0 {
                return false;
            }
            exists[num as usize - 1] = 1; 
        } 
 
        for j in exists { 
            if j != 1 { 
                return false; 
            } 
        } 
 
        for j in exists.iter_mut() { *j = 0; } 
    } 
 
    true 
}

fn cook() {
    let cook = "⠀⠀⢀⣴⣿⣿⣷⣦⣌⠛⢦⡀⠀⠈⠓⢦⣀⡀⠀⣸⣿⣿⣿⡀⠀\n\
    ⠀⠀⡾⠋⠉⢿⣿⣿⡿⠟⠦⣝⡲⣄⣀⠀⠈⠉⠉⣽⡿⢿⣿⡇⠀\n\
    ⠀⠀⣷⠀⣠⣿⡿⠋⠀⠀⣶⢤⣙⠳⢭⣙⠲⠤⠴⠋⠑⠀⠁⣧⠀\n\
    ⠀⠀⢸⡼⠛⠛⠀⠀⠀⣼⠉⢿⣿⣧⣶⡿⠛⠶⢤⣀⠀⠀⠀⣻ \n\
    ⠀⠀⢨⡇⠀⠀⠀⠀⠀⠈⠉⠉⢸⡟⣺⠃⠀⠀⠀⠈⠙⠲⠶⠋⠀\n\
    ⠀⠀⣸⠁⠀⠀⠀⠀⠀⢀⡀⠀⢸⡷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\
    ⠀⣰⠃⠀⠀⠀⠠⣄⡀⠀⠉⣳⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀WHO LET HIM COOK\n\
    ⣞⠁⠀⠲⣄⠀⠀⠀⠉⠉⡷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\
    ⣌⠳⣤⡀⠈⠓⠦⢤⡴⠚⠁⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀\n\
    ⣿⣷⣤⡿⢷⠀⣀⡴⣷⠒⠒⢒⣶⢤⠞⠉⠙⢻⣿⣷⣄⠀⠀⠀⠀\n\
    ⠙⠻⣿⣷⠈⠛⠙⡇⣿⠀⠀⢯⣽⢿⠀⠀⠀⣴⠚⠉⠛⠀⠀⠀⠀\n\
    ⣶⣆⠀⢹⣠⠶⣄⡇⢻⠛⠓⠒⠚⠋⠙⠓⠲⠮⠿⠆⠀⠀⠀⠀⠀\n\
    ⣿⣿⠀⢸⠙⠒⢃⣇⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n";
    print!("{}", cook);
}

fn cook_harder() {
    let cook_harder = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⣠⠞⠉⢉⠩⢍⡙⠛⠋⣉⠉⠍⢉⣉⣉⣉⠩⢉⠉⠛⠲⣄⠀⠀⠀⠀\n\
    ⠀⠀⠀⡴⠁⠀⠂⡠⠑⠀⠀⠀⠂⠀⠀⠀⠀⠠⠀⠀⠐⠁⢊⠀⠄⠈⢦⠀⠀⠀\n\
    ⠀⣠⡾⠁⠀⠀⠄⣴⡪⠽⣿⡓⢦⠀⠀⡀⠀⣠⢖⣻⣿⣒⣦⠀⡀⢀⣈⢦⡀⠀\n\
    ⣰⠑⢰⠋⢩⡙⠒⠦⠖⠋⠀⠈⠁⠀⠀⠀⠀⠈⠉⠀⠘⠦⠤⠴⠒⡟⠲⡌⠛⣆\n\
    ⢹⡰⡸⠈⢻⣈⠓⡦⢤⣀⡀⢾⠩⠤⠀⠀⠤⠌⡳⠐⣒⣠⣤⠖⢋⡟⠒⡏⡄⡟  COOK HARDER\n\
    ⠀⠙⢆⠀⠀⠻⡙⡿⢦⣄⣹⠙⠒⢲⠦⠴⡖⠒⠚⣏⣁⣤⣾⢚⡝⠁⠀⣨⠞⠀\n\
    ⠀⠀⠈⢧⠀⠀⠙⢧⡀⠈⡟⠛⠷⡾⣶⣾⣷⠾⠛⢻⠉⢀⡽⠋⠀⠀⣰⠃⠀⠀\n\
    ⠀⠀⠀⠀⠑⢤⡠⢂⠌⡛⠦⠤⣄⣇⣀⣀⣸⣀⡤⠼⠚⡉⢄⠠⣠⠞⠁⠀⠀⠀\n\
    ⠀⠀⠀⠀⠀⠀⠉⠓⠮⣔⡁⠦⠀⣤⠤⠤⣤⠄⠰⠌⣂⡬⠖⠋⠀⠀⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠤⢤⣀⣀⡤⠴⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n";
    print!("{}", cook_harder);
}

fn cooked() {
    let cooked = "⢻⣿⡗⢶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣄\n\
    ⠀⢻⣇⠀⠈⠙⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠛⠋⣹⣿⡿\n\
    ⠀⠀⠹⣆⠀⠀⠀⠀⠙⢷⣄⣀⣀⣀⣤⣤⣤⣄⣀⣴⠞⠋⠉⠀⠀⠀⢀⣿⡟⠁\n\
    ⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀\n\
    ⠀⠀⠀⠀⠈⠻⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣠⡾⠋⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⠀⣼⠃⠀⢠⠒⣆⠀⠀⠀⠀⠀⠀⢠⢲⣄⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⢰⡏⠀⠀⠈⠛⠋⠀⢀⣀⡀⠀⠀⠘⠛⠃⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⣾⡟⠛⢳⠀⠀⠀⠀⠀⣉⣀⠀⠀⠀⠀⣰⢛⠙⣶⠀⢹⣇⠀⠀⠀⠀ flag is grey{your_input_here} :)\n\
    ⠀⠀⠀⠀⢿⡗⠛⠋⠀⠀⠀⠀⣾⠋⠀⢱⠀⠀⠀⠘⠲⠗⠋⠀⠈⣿⠀⠀⠀⠀\n\
    ⠀⠀⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠈⠓⠒⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀\n\
    ⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀\n";
    print!("{}", cooked);
}
