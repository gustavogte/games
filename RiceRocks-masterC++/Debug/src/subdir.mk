################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/Bullet.cpp \
../src/Game.cpp \
../src/RiceRocks.cpp \
../src/Rock.cpp \
../src/SDLsetup.cpp \
../src/Ship.cpp \
../src/Sprite.cpp 

OBJS += \
./src/Bullet.o \
./src/Game.o \
./src/RiceRocks.o \
./src/Rock.o \
./src/SDLsetup.o \
./src/Ship.o \
./src/Sprite.o 

CPP_DEPS += \
./src/Bullet.d \
./src/Game.d \
./src/RiceRocks.d \
./src/Rock.d \
./src/SDLsetup.d \
./src/Ship.d \
./src/Sprite.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


