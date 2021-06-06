################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.cc \
../tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.cc 

CC_DEPS += \
./tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.d \
./tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.d 

OBJS += \
./tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.o \
./tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.o 


# Each subdirectory must supply rules for building sources it contributes
tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.o: ../tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.cc
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DUSE_HAL_DRIVER -DDEBUG -DSTM32F407xx -c -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/flatbuffers" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/gemmlowp" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/ruy" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/tensorflow" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"tensorflow_lite/tensorflow/lite/micro/memory_planner/greedy_memory_planner.d" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"
tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.o: ../tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.cc
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DUSE_HAL_DRIVER -DDEBUG -DSTM32F407xx -c -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/flatbuffers" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/gemmlowp" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/ruy" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/tensorflow" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"tensorflow_lite/tensorflow/lite/micro/memory_planner/linear_memory_planner.d" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

