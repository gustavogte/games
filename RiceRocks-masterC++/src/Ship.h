/*
 * Ship.h

 *
 *      Author: Diego Charrez
 */
#include "Sprite.h"


#ifndef SHIP_H_
#define SHIP_H_

class Ship{
public:
	Ship(SDLsetup *);
	virtual ~Ship();
	//void shoot();
	void move();

	void draw();
	void update();

	bool moveRight;
	bool moveLeft;
	bool moveUp;
	bool moveDown;

	Sprite * ship;

	int getShipX();
	int getShipY();

private:

	int timeCheck;
	SDLsetup * setup;
};

#endif /* SHIP_H_ */
