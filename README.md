# Bullet Mania

Welcome to the Bullet Mania source code!

Bullet Mania is a pixel-art, shooting video game made with Pygame (Community Edition). It's a work-in-progress project made with the intent of showing to our Programming Teacher the skills we apprehended in these 3 years of school.

The game is, up to now, made of a large map which holds the local player and the AI bots. Each session is hordes-oriented, with each horde having progressively harder to beat bots.

Have fun! 🧡
## Run Locally

Running the game locally is as easy as drinking a glass of water!

Clone the project

```bash
  git clone https://github.com/LiceoDaVinciJesi-3AS-2025-2026/Bullet-Mania.git
```

Go to the project directory

```bash
  cd Bullet-Mania
```

Run the game

```bash
  uv run bullet-mania
```


## Optimizations

The game's lowest FPS are around 140 frames/second registered on a machine with an Intel i5-9400F and 8GB of RAM.

The game runs on various optimizations, such as:
- Frustum Culling (don't draw entities that are not within the player's camera frustum),
- Data Oriented Design (objects data preferred over classes),
- Batch Rendering (draw entities all at once through `surface.blits`)

## Credits

- Tiles, sprites and UIs made by [@Morress](https://github.com/Morress) through Piskel and Blender,
- Gun System, Bots and Tiles code made by [@ItzLucio](https://github.com/ItzLucio),
- Waves code made by [@Morress](https://github.com/Morress)


## Authors

- [@Morress](https://github.com/Morress)
- [@ItzLucio](https://github.com/ItzLucio)