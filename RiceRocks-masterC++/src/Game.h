/*
 * Game.h
 *
 *      Author: Diego Charrez
 */

#ifndef GAME_H_
#define GAME_H_
#include "stdafx.h"
#include "SDLsetup.h"
#include "Sprite.h"
#include "Ship.h"
#include "Rock.h"
#include "Bullet.h"

#include <string>
#include <sstream>

class Game {
public:
	Game(int width,int heigh);
	virtual ~Game();
	void gameLoop();
	void createArmageddon();
	void bullets();


	bool checkCollisions(SDL_Rect a, SDL_Rect b);
	void collisionShipRock(Ship *, vector<Rock *>);
	void collisionBulletRock(vector<Bullet *>, vector<Rock *>);


private:
	int points;
	bool quit;
	Sprite * background;
	SDLsetup * setup;
	Ship * ship;

	vector<Rock *> armageddon;
	vector<Bullet *> shots;

	Bullet * shot;

	int lives;
	int score;

	string Score;
	string Lives;


	int rockMotion;

	int timeCheck;
	int bulletSpeed;
	int screenWidth;
	int screenHeight;

	bool attack;

	bool moveRight;
	bool moveLeft;
	bool moveUp;
	bool moveDown;
};

#endif /* GAME_H_ */
