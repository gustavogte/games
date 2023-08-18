/*
 * Rock.h
 *
 *  Created on: Oct 24, 2014
 *      Author: ddc
 */

#ifndef ROCK_H_
#define ROCK_H_
#include "SDLsetup.h"
#include "Sprite.h"

class Rock {
private:

	SDLsetup * setup;
	int timeCheck;
	int randomW;
	int randomH;
	int angle;
public:
	Rock(SDLsetup * setup, int width, int height);

	Sprite * rock;


	virtual ~Rock();
	void draw();
	void randomMotionDown();
	void randomMotionLeftO();
	void randomMotionRightO();
};

#endif /* ROCK_H_ */
