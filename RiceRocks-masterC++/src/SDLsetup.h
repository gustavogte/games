/*
 * SDLsetup.h
 *
 *  Created on: Oct 15, 2014
 *      Author: ddc
 */

#include "stdafx.h"
#ifndef SDLSETUP_H_
#define SDLSETUP_H_

class SDLsetup {
private:
	SDL_Window *window;
	SDL_Renderer *renderer;
	SDL_Event *mainEvent;
public:
	SDLsetup();
	SDLsetup(bool *quit,int,int);
	virtual ~SDLsetup();
	SDL_Renderer * getRenderer();
	SDL_Event * getMainEvent();

	SDL_Surface * surface;
	SDL_Texture * texture;
	SDL_Rect dstrect;

	TTF_Font * font;

	void writeText(string text, int x, int y);
	void drawText();

	void  begin();
	void  end();
};

#endif /* SDLSETUP_H_ */
