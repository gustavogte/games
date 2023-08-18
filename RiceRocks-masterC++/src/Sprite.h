/*
 * Sprite.h
 *
 *  Created on: Oct 19, 2014
 *      Author: ddc
 */

#ifndef SPRITE_H_
#define SPRITE_H_
#include "SDLsetup.h"
#include "stdafx.h"


class Sprite {
public:
	Sprite();
	Sprite(SDL_Renderer *,std::string,int x,int y,int w,int h);
	virtual ~Sprite();

	void setX(int X);
	void setY(int Y);
	void setPosition(int,int);
	int getX();
	int getY();
	int getW();
	int getH();

	void draw();

	SDL_Texture * getTexture();
	SDL_Rect getRect();
	SDL_Renderer*  getRenderer();

	void setTexture(SDL_Texture*);
	void setRect(SDL_Rect);
	void setRenderer(SDL_Renderer*);



private:
	SDL_Rect rect;
	SDL_Texture * image;
	SDL_Renderer * renderer;
};

#endif /* SPRITE_H_ */
