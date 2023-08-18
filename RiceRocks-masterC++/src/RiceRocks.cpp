//============================================================================
// Author      : Diego Charrez
// Version     : RiceRocks 1.0
//============================================================================
#include "stdafx.h"

using namespace std;
#include "Game.h"
#include "Ship.h"

int main( int argc, char* argv[] )
	{
		Game * game = new Game(640,480);
		game->gameLoop();
		delete game;
		return 0;
	}
