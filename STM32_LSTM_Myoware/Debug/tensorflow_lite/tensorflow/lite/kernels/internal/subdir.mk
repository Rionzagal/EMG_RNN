################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.cc 

CC_DEPS += \
./tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.d 

OBJS += \
./tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.o 


# Each subdirectory must supply rules for building sources it contributes
tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.o: ../tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.cc
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DUSE_HAL_DRIVER -DDEBUG -DSTM32F407xx -c -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/flatbuffers" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/gemmlowp" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party/ruy" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/third_party" -I"D:/STM32F407 Projects/STM32_LSTM_Myoware/tensorflow_lite/tensorflow" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"tensorflow_lite/tensorflow/lite/kernels/internal/quantization_util.d" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

