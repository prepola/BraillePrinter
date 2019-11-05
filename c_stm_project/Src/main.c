/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stdio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
TIM_HandleTypeDef htim9;

UART_HandleTypeDef huart6;

/* USER CODE BEGIN PV */
int UARTARREY=0;
int i[] = {0,0,0};
int NextAddSpaceCount =0;
int beforeCount =0;
int EnterCount=0;
int j=0;
int EnterSignal=0;
int SwitchCount=0;
uint8_t rx3_data;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM9_Init(void);
static void MX_USART6_UART_Init(void);
/* USER CODE BEGIN PFP */
int doc_servo(int *i);
void step_plus_1pulse();
void step_minus_1pulse();
void step_Space();
void step_Next();
void step_Enter();
void step_before();
void Print();
void before_Check();
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */
  

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM9_Init();
  MX_USART6_UART_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_PWM_Start(&htim9, TIM_CHANNEL_1);
  HAL_UART_Receive_IT(&huart6, &rx3_data, 1);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  step_Enter();



		  switch(rx3_data)
		  				  {
		  				  case '1':
		  					  i[0]=0;
		  					  i[1]=0;
		  					  i[2]=0;
		  					  break;

		  				  case '2':
		  					  i[0]=0;
		  					  i[1]=0;
		  					  i[2]=1;
		  					  break;

		  				  case '3':
		  					  i[0]=0;
		  					  i[1]=1;
		  					  i[2]=0;
		  					  break;

		  				  case '4':
		  					  i[0]=0;
		  					  i[1]=1;
		  					  i[2]=1;
		  					  break;

		  				  case '5':
		  					  i[0]=1;
		  					  i[1]=0;
		  					  i[2]=0;
		  					  break;

		  				  case '6':
		  					  i[0]=1;
		  					  i[1]=0;
		  					  i[2]=1;
		  					  break;

		  				  case '7':
		  					  i[0]=1;
		  					  i[1]=1;
		  					  i[2]=0;
		  					  break;

		  				  case '8':
		  					  i[0]=1;
		  					  i[1]=1;
		  					  i[2]=1;
		  					  break;

		  				  case '9':
		  					 EnterSignal=1;
		  					 break;

		  				  default:
		  					  HAL_Delay(10);
		  				  }
		  printf("%d:%d:%d\r\n",i[0],i[1],i[2]);
		  NextAddSpaceCount++;
		  				if(NextAddSpaceCount==37)	//가로로 꽉 찼을 경우 다음줄로 넘어가는 함수
		  					 {
		  						 for(int a=beforeCount; a>0;a--)
		  						 {
		  						 step_before();
		  						 HAL_Delay(10);
		  						 }
		  						 HAL_Delay(1000);
		  						 step_Enter();
		  						 HAL_Delay(1000);
		  						 EnterCount++;
		  						 NextAddSpaceCount=1;
		  					 }

		  				else if(EnterSignal ==1)	//가로로 글을 꽉 안채우고 다음줄로 넘어갈 경우의 신호
							 {
								 for(int a=beforeCount; a>0;a--)
								 {
								 step_before();
								 HAL_Delay(10);
								 }
								 HAL_Delay(1000);
								 step_Enter();
								 HAL_Delay(1000);
								 HAL_Delay(200);
								 EnterCount++;
								 NextAddSpaceCount=1;
								 EnterSignal=0;
							 }
		  				int temp = doc_servo(i);
		  				__HAL_TIM_SET_COMPARE(&htim9, TIM_CHANNEL_1, temp);
		  				 HAL_Delay(1000);

		  				Print();
		  				if(NextAddSpaceCount%2==1)		//한 자음에서 3:3중 다음 3개의 점찍을때의 띄어쓰기
							 {
								 step_Next();
								 HAL_Delay(1000);
								 HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_5);
								 beforeCount++;
							 }
							 else if(NextAddSpaceCount%2==0)	//다음 자음으로 넘어가기
								{
								 step_Space();
								 HAL_Delay(1000);
								 HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_5);
								 beforeCount=beforeCount+2;
								}

							 else if(EnterCount==19)	// 한장 다하면 모터들 종료 추후 수정 (ex: 다음장까지 얼마나 돌아야하나 등으로)
							 {
								 step_Enter();
								 HAL_Delay(200);
								 step_Enter();
								 HAL_Delay(200);
								 step_Enter();
								 HAL_Delay(200);
								 HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_SET);
								 HAL_GPIO_WritePin(GPIOC,GPIO_PIN_1,GPIO_PIN_RESET);
							 }

		  					}

  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage 
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief TIM9 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM9_Init(void)
{

  /* USER CODE BEGIN TIM9_Init 0 */

  /* USER CODE END TIM9_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM9_Init 1 */

  /* USER CODE END TIM9_Init 1 */
  htim9.Instance = TIM9;
  htim9.Init.Prescaler = 840;
  htim9.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim9.Init.Period = 1999;
  htim9.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim9.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim9) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim9, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim9) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 999;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim9, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM9_Init 2 */

  /* USER CODE END TIM9_Init 2 */
  HAL_TIM_MspPostInit(&htim9);

}

/**
  * @brief USART6 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART6_UART_Init(void)
{

  /* USER CODE BEGIN USART6_Init 0 */

  /* USER CODE END USART6_Init 0 */

  /* USER CODE BEGIN USART6_Init 1 */

  /* USER CODE END USART6_Init 1 */
  huart6.Instance = USART6;
  huart6.Init.BaudRate = 115200;
  huart6.Init.WordLength = UART_WORDLENGTH_8B;
  huart6.Init.StopBits = UART_STOPBITS_1;
  huart6.Init.Parity = UART_PARITY_NONE;
  huart6.Init.Mode = UART_MODE_TX_RX;
  huart6.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart6.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart6) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART6_Init 2 */

  /* USER CODE END USART6_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_0|GPIO_PIN_1|LD2_Pin|GPIO_PIN_8 
                          |GPIO_PIN_9|GPIO_PIN_10, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4|GPIO_PIN_5, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : PC1 */
  GPIO_InitStruct.Pin = GPIO_PIN_1;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : PA0 PA1 LD2_Pin PA8 
                           PA9 PA10 */
  GPIO_InitStruct.Pin = GPIO_PIN_0|GPIO_PIN_1|LD2_Pin|GPIO_PIN_8 
                          |GPIO_PIN_9|GPIO_PIN_10;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : USART_TX_Pin USART_RX_Pin */
  GPIO_InitStruct.Pin = USART_TX_Pin|USART_RX_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF7_USART2;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : PC9 */
  GPIO_InitStruct.Pin = GPIO_PIN_9;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : PB4 PB5 */
  GPIO_InitStruct.Pin = GPIO_PIN_4|GPIO_PIN_5;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */



int _write(int file,char *ptr, int len)
{
	int dataIdx;
	for(dataIdx =0; dataIdx < len; dataIdx++)
	{
		ITM_SendChar(*ptr++);
	}
	return len;
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if(huart->Instance ==USART6)
	{
		HAL_UART_Receive_IT(&huart6, &rx3_data,1);
		HAL_UART_Transmit(&huart6, &rx3_data,1,10);

	}
}

int doc_servo(int *i)
{
	 if(i[0]==0)
	  {
		  if(i[1]==0)
		  {
			  if(i[2]==0)	//000
			  {
				  j=55;
			  }
			  else if(i[2]==1)	//001
			  {
				  j=158;
			  }
		  }
		  else if(i[1]==1)
		  {
			  if(i[2]==0)	//010
			  {
				  j=108;
			  }
			  else if(i[2]==1)	//011
			  {
				  j=208;
			  }
		  }
	  }
	  else if(i[0]==1)
	  {
		  if(i[1]==0)
		  {
			  if(i[2]==0)	//100
			  {
				  j=79;
			  }
			  else if(i[2]==1)	//101
			  {
				  j=180;
			  }
		  }
		  else if(i[1]==1)
		  {
			  if(i[2]==0)	//110
			  {
				  j=128;
			  }
			  else if(i[2]==1)	//111
			  {
				  j=235;
			  }
		  }
	  }
 return j;
}

void Print()
{
	  HAL_GPIO_WritePin(GPIOC,GPIO_PIN_1,GPIO_PIN_SET);
	  HAL_GPIO_WritePin(GPIOA,GPIO_PIN_0,GPIO_PIN_RESET);
	  HAL_GPIO_WritePin(GPIOA,GPIO_PIN_1,GPIO_PIN_SET);
	  HAL_Delay(3500);
	  HAL_GPIO_WritePin(GPIOA,GPIO_PIN_0,GPIO_PIN_SET);
	  HAL_GPIO_WritePin(GPIOA,GPIO_PIN_1,GPIO_PIN_RESET);
	  HAL_Delay(4100);
	  printf("dc모터로 쾅\r\n");

}

void step_plus_1pulse()
{
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_SET);
	HAL_Delay(1);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_RESET);
	HAL_Delay(1);
}

void step_minus_1pulse()
{
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_SET);
	HAL_Delay(1);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_RESET);
	HAL_Delay(1);
}

void step_Next()
{
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_RESET);
	for(int a=0; a<350; a++)
		  {
			  step_plus_1pulse();
			  if(a==349)
			  {
				  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_SET);
			  }
		  }
	printf("다음껄로 넘어가\r\n");
}

void step_before()
{
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_RESET);

			  step_minus_1pulse();

			  if(HAL_GPIO_ReadPin(GPIOC,GPIO_PIN_9)==GPIO_PIN_RESET)	//눌렸을때
			  {
				  printf("첫번째 스위치 눌림\r\n");
				  step_Next();
				  before_Check();

			  }

	printf("전에껄로 넘어가\r\n");
}

void before_Check()
{
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_RESET);

	  for(int g=0; g<10000; g++)
	  {
			step_minus_1pulse();
			  if(HAL_GPIO_ReadPin(GPIOC,GPIO_PIN_9)==GPIO_PIN_RESET)
			  {
				  printf("두번째 스위치 눌림\r\n");
				  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_SET);
			  }
	  }



}

void step_Space()
{
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_RESET);
	for(int a=0; a<700; a++)
		  {
			  step_plus_1pulse();
			  if(a==699)
			  {
				  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_SET);
			  }
		  }
	printf("스페이스다\r\n");
}

void step_Enter()
{
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_RESET);
	for(int a=0; a<130; a++)
			  {
				HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8,GPIO_PIN_SET);
				HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, GPIO_PIN_SET);
				HAL_Delay(1);
				HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, GPIO_PIN_RESET);
				HAL_Delay(1);

				  if(a==129)
				  {
					  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9,GPIO_PIN_SET);
				  }
			  }
	printf("엔터다\r\n");

}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
