//@ts-check

class Level1Scene extends Phaser.Scene {
  /** Load assets into RAM */
  preload() {
    this.load.image('sky', 'assets/sky.png');
    this.load.image('ground', 'assets/platform.png');
    this.load.image('star', 'assets/star.png');
    this.load.image('bomb', 'assets/bomb.png');
    this.load.spritesheet('dude', 'assets/dude.png', { frameWidth: 32, frameHeight: 48 });
  }

  /** Create and initialize scene components */
  create() {
    this.gameOver = false;
    this.score = 0;
    this.ggwave = 10000000;
    this.hihihaha = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 196, 180, 45, 13, 53, 112, 133, 142, 221, 121, 3, 157, 113, 81, 80, 195, 253, 225, 197, 202, 197, 48, 46, 21, 121, 40, 23, 239, 35, 175, 254, 103, 36, 126, 183, 218, 112, 235, 9, 98, 99, 29, 109, 196, 120, 43, 68, 126, 100, 81]

    //  A simple background for our game
    this.add.image(400, 300, 'sky');
  
    //  The platforms group contains the ground and the 2 ledges we can jump on
    this.platforms = this.physics.add.staticGroup();
  
    //  Here we create the ground.
    //  Scale it to fit the width of the game (the original sprite is 400x32 in size)
    this.platforms.create(400, 568, 'ground').setScale(2).refreshBody();
  
    // The player and its settings
    this.player = this.physics.add.sprite(100, 450, 'dude');
  
    //  Player physics properties. Give the little guy a slight bounce.
    this.player.setCollideWorldBounds(true);
  
    //  Our player animations, turning, walking left and walking right.
    this.anims.create({
      key: 'left',
      frames: this.anims.generateFrameNumbers('dude', { start: 0, end: 3 }),
      frameRate: 10,
      repeat: -1
    });
  
    this.anims.create({
      key: 'turn',
      frames: [{ key: 'dude', frame: 4 }],
      frameRate: 20
    });
  
    this.anims.create({
      key: 'right',
      frames: this.anims.generateFrameNumbers('dude', { start: 5, end: 8 }),
      frameRate: 10,
      repeat: -1
    });
  
    //  Input Events
    this.cursors = this.input.keyboard.createCursorKeys();
  
    //  Some stars to collect, 12 in total, evenly spaced 70 pixels apart along the x axis
    this.sauces = this.physics.add
    this.stars = this.physics.add.group({
      key: 'star',
      repeat: 11,
      setXY: { x: 12, y: 0, stepX: 70 }
    });
    this.stars.children.iterate(function (child) {
        //  Give each star a slightly different bounce
        child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
    });
  
    this.bombs = this.physics.add.group();

    for (let i = 0; i < 5; ++i) {
      var bomb = this.bombs.create(i * 30, 16, 'bomb');
      bomb.setBounce(0.5);
      bomb.setCollideWorldBounds(true);
      bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
      bomb.allowGravity = false;
      
      var bomb2 = this.bombs.create(800 - i * 30, 16, 'bomb');
      bomb2.setBounce(0.5);
      bomb2.setCollideWorldBounds(true);
      bomb2.setVelocity(Phaser.Math.Between(-200, 200), 20);
      bomb2.allowGravity = false;
    }
  
    //  The score
    this.scoreText = this.add.text(16, 16, 'Wave: 0', { fontSize: '32px', color: '#000' });
  
    //  Collide the player and the stars with the platforms
    this.physics.add.collider(this.player, this.platforms);
    this.physics.add.collider(this.stars, this.platforms);
    this.physics.add.collider(this.bombs, this.platforms);
  
    //  Checks to see if the player overlaps with any of the stars, if he does call the collectStar function
    this.physics.add.overlap(this.platforms, this.stars, this.collectStar, null, this);
    this.physics.add.overlap(this.player, this.stars, this.collectStar, null, this);
  
    this.physics.add.collider(this.player, this.bombs, this.hitBomb, null, this);
  }

  /** runs in a loop, used to check for input changes */
  update() {
    if (this.gameOver) {
      return;
    }
  
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
  
      this.player.anims.play('left', true);
    }
    else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
  
      this.player.anims.play('right', true);
    }
    else {
      this.player.setVelocityX(0);
  
      this.player.anims.play('turn');
    }

    if (this.cursors.up.isDown && this.player.body.touching.down)
    {
      this.player.setVelocityY(-330);
    }
  
    // spawn star
  }
  
  collectStar(player, star) {
    star.disableBody(true, true);
  
    if (this.stars.countActive(true) === 0) {
      //  Add and update the score
      this.score += 1;
      this.scoreText.setText('Wave: ' + this.score);

      //  A new batch of stars to collect
      this.stars.children.iterate(function (star) {
        star.enableBody(true, star.x, 0, true, true);
        return true;
      });  

      this.bombs.children.iterate(function (bomb) {
        bomb.setPosition(bomb.x, 0);
        bomb.setBounce(0.5);
        bomb.setCollideWorldBounds(true);
        bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
        bomb.allowGravity = false;
        return true;
      });

      // exponentiation
      let base = this.hihihaha.reduce((acc, cur) => (acc << 8n) + BigInt(cur), 0n);
      let exp = 65537;
  
      let p = BigInt("2933342412243178360246913963653176924656287769470170577218737")
      let q = BigInt("2663862733012296707089609302317500558193537358171126836499053")
      let modulus = p * q
  
      let result = 1n;
  
      for (let i = 0; i < exp; i++) result = (result * base) % modulus;
      for (let i = 0; i < 64; ++i) {
        this.hihihaha[this.hihihaha.length-1-i] = Number(result & 0xffn);
        result = result >> 8n;
      }
  
      // scrambling
      for (let i = this.hihihaha.length-1; i >= 24; i--) {
        let ri = ((i * this.score) % 40) + 24;
        [this.hihihaha[i], this.hihihaha[ri]] = [this.hihihaha[ri], this.hihihaha[i]];
      }
  
      // xor
      let key = this.score & 0xff;
      for (let i = 24; i < this.hihihaha.length; ++i) {
        this.hihihaha[i] ^= key;
        key = this.hihihaha[i];
      }

      if (this.score == this.ggwave) {
        let flag = this.hihihaha.map(n => String.fromCharCode(n)).join("")
        console.log(flag.slice(16))
      }
    }
  }
  
  hitBomb(player, bomb) {
    this.physics.pause();
  
    player.setTint(0xff0000);
  
    player.anims.play('turn');
  
    this.gameOver = true;
  }
}

var config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 300 },
      debug: false
    }
  },
  scene: Level1Scene
};

var game = new Phaser.Game(config);

