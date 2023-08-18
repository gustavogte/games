/*
 * Bullet.h
 *
 *  Created on: Nov 2, 2014
 *      Author: ddc
 */

#ifndef BULLET_H_
#define BULLET_H_
#include "SDLsetup.h"
#include "Sprite.h"
#include "Ship.h"

class Bullet{
private:

	SDLsetup * setup;
	unsigned int bulletSpeed;
public:

	Bullet(SDLsetup * setup, int x , int y);
	virtual ~Bullet();

	Sprite * bullet;

	void Draw();
	void Shoot();

};

#endif /* BULLET_H_ */
