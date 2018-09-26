using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Threading;

// TODO opção de definir probabilidade da mutação deletéria em cada infecção, de acordo com o ciclo determinado (trabalhar com intervalos)
// esta probabilidade estará sempre atrelada ao ciclo de infecção
// TODO BUG para poucas partículas, porcentagem de partículas que descem de classe pode dar mais de 100%, pois cálculo é feito
// no final do código, e o valor utilizado para o código é o da mutação
// TODO *** avaliar quando encerrar um paciente e passar para o próximo (média das classes for constante)
// TODO fazer simulação definindo em quais ciclos ocorrem infecções
// TODO interface gráfica (gráficos em tempo real, novas janelas para cada paciente etc)

// TODO: A INTRO explanation about this program, the main use, the aim, how it works, the output and what to do with.


namespace multi_dimensional_array
{
	public class ProgramMarcos3D
	{
		// Number of Cycles
		public const int Cycle = 51;

		// Number of Classes
		public const int Class = 11;

		// Number of Patients
		public const int Generations = 16;

		static int[] InfectionCycle = new int[Generations];

		//static int[,,] ParticlesThatInfected = new int[Generations, Cycle, Class];

		// The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
		public const int InitialParticles = 5;

		public const int MaxParticles = 1000000; // Limite máximo de partículas que quero impor para cada ciclo (linha)

		//public const double DeleteriousProbability = 0.9;
		//public const double BeneficialProbability = 0.005;

		static double[] DeleteriousProbability = new double[Cycle];
		static double[] BeneficialProbability = new double[Cycle];

		public const bool BeneficialIncrement = false; // if true, beneficial probability will increase by INCREMENT each cycle
		// if false, it will change from a fixed value to another fixed value, at the chosen cycle
		public const bool DeleteriousIncrement = false; // if true, deleterious probability will increase by INCREMENT each cycle
		// if false, it will change from a fixed value to another fixed value, at the chosen cycle

		// NOT USED YET
		//public const int BottleneckParticles = 10;

		// Lists to keep the number of particles that go up or down the classes, during mutations
		static int[,] ClassUpParticles = new int[Generations, Cycle];
		static int[,] ClassDownParticles = new int[Generations, Cycle];

		static void Main(string[] args)
		{
			Random rnd = new Random();
			
			// create and start the Stopwatch Class. From: https://msdn.microsoft.com/en-us/library/system.diagnostics.stopwatch
			Stopwatch stopWatch = new Stopwatch();
			stopWatch.Start();
			//Thread.Sleep(10000);

			FillInfectionCycleArray(4, 10, 20, 40); // FIRST PARAMETER: initial cycle, SECOND PARAMENTER: increment

			if (DeleteriousIncrement)
			{
				FillDeleteriousArrayWithIncrement(0.3, 0.1); // FIRST PARAMETER: initial probability, SECOND PARAMENTER: increment
			}
			else
			{
				FillDeleteriousArray(/*0.1, */0.3, 0.8, 8/*, 17*/); // FIRST PARAMETER: first probability, SECOND PARAMENTER: second probability
				// THIRD PARAMETER: cycle to change from first probability to second probability
			}

			if (BeneficialIncrement)
			{
				FillBeneficialArrayWithIncrement(0.0003, 0.0001); // FIRST PARAMETER: initial probability, SECOND PARAMENTER: increment
			}
			else
			{
				FillBeneficialArray(0.0001, 0.0001, 10); // FIRST PARAMETER: first probability, SECOND PARAMENTER: second probability
													// THIRD PARAMETER: cycle to change from first probability to second probability
			}


			// Declaring the three-dimensional Matrix: it has p Generations, x lines of Cycles and y columns of Classes, defined by the variables above. 
			int[,,] Matrix = new int[Generations, Cycle, Class];

			// The Matrix starts on the Generations 0, 10th position (column) on the line zero. 
			// The "InitialParticles" is the amount of viral particles that exists in the class 10 on the cycle zero.
			// That is: these 5 particles have the potential to create 10 particles each.
			Matrix[0, 0, 10] = InitialParticles;

			RunPatients(Matrix, rnd);

			stopWatch.Stop();
			// Get the elapsed time as a TimeSpan value.
			TimeSpan ts = stopWatch.Elapsed;

			PrintOutput(Matrix);

			// Format and display the TimeSpan value.
			string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);
			Console.WriteLine("Total Run Time: " + elapsedTime);
			Console.Write("\n");
			Console.ReadKey();
		}

		static void FillInfectionCycleArray(int Cycle1, int Cycle2, int Cycle3, int Cycle4)
		{
			Random rndI = new Random();

			for (int i = 0; i < InfectionCycle.GetLength(0); i++)
			{
				int RandomNumberI = rndI.Next(1, 5);

				if (RandomNumberI == 1)
				{
					InfectionCycle[i] = Cycle1;
				}

				if (RandomNumberI == 2)
				{
					InfectionCycle[i] = Cycle2;
				}

				if (RandomNumberI == 3)
				{
					InfectionCycle[i] = Cycle3;
				}

				if (RandomNumberI == 4)
				{
					InfectionCycle[i] = Cycle4;
				}

			}
		}

		static void FillDeleteriousArray(double FirstProbability, double SecondProbability, /*double ThirdProbability,*/int ChangeCycle1/*, int ChangeCycle2*/)
		{
			for (int i = 0; i < DeleteriousProbability.GetLength(0); i++)
			{
				if (i <= ChangeCycle1)
				{
					DeleteriousProbability[i] = FirstProbability;
				}
				if (i > ChangeCycle1/* && i <= ChangeCycle2*/)
				{
					DeleteriousProbability[i] = SecondProbability;
				}
				//if (i > ChangeCycle2)
				//{
				//	DeleteriousProbability[i] = ThirdProbability;
				//}
			}
		}

		static void FillDeleteriousArrayWithIncrement(double InitialProbability, double Increment)
		{
			for (int i = 0; i < DeleteriousProbability.GetLength(0); i++)
			{
				if (i == 0)
				{
					DeleteriousProbability[i] = InitialProbability;
				}
				else
				{
					if (DeleteriousProbability[i - 1] + Increment <= (1 - BeneficialProbability.GetLength(0)))
					{
						DeleteriousProbability[i] = DeleteriousProbability[i - 1] + Increment;
					}
					else
					{
						DeleteriousProbability[i] = DeleteriousProbability[i - 1];
					}
				}
			}
		}

		static void FillBeneficialArray(double FirstProbability, double SecondProbability, int ChangeCycle)
		{
			for (int i = 0; i < BeneficialProbability.GetLength(0); i++)
			{
				if (i <= ChangeCycle)
				{
					BeneficialProbability[i] = FirstProbability;
				}
				else
				{
					BeneficialProbability[i] = SecondProbability;
				}
			}
		}

		static void FillBeneficialArrayWithIncrement(double InitialProbability, double Increment)
		{
			for (int i = 0; i < BeneficialProbability.GetLength(0); i++)
			{
				if (i == 0)
				{
					BeneficialProbability[i] = InitialProbability;
				}
				else
				{
					if (BeneficialProbability[i - 1] + Increment <= (1 - DeleteriousProbability.GetLength(0)))
					{
						BeneficialProbability[i] = BeneficialProbability[i - 1] + Increment;
					}
					else
					{
						BeneficialProbability[i] = BeneficialProbability[i - 1];
					}
				}
			}
		}

		static void RunPatients(int[,,] Matrix, Random rndx)
		{
			// Main Loop to create more particles on the next Cycles from the Cycle Zero (lines values).
			// Each matrix position will bring a value. This value will be mutiplied by its own class number (column value). 
			for (int p = 0; p < Generations; p++)
			{
				for (int i = 0; i < Cycle; i++)
				{
					for (int j = 0; j < Class; j++)
					{
						if (i > 0)
						{
							// Multiplies the number os particles from de previous Cycle by the Class number which belongs.
							// This is the progeny composition.
							Matrix[p, i, j] = Matrix[p, (i - 1), j] * j;
						}
					}

					CutOffMaxParticlesPerCycle(Matrix, p, i, rndx);
					ApplyMutationsProbabilities(Matrix, p, i);

					if (i == InfectionCycle[p] && p < (Matrix.GetLength(0) - 1))
					{
						//Console.WriteLine(Matrix.GetLength(0));
						PickRandomParticlesForInfection(Matrix, p, i, rndx);
						Console.WriteLine("*** INFECTION CYCLE *** {0}", i);
					}

					// print which Cycle was finished just to give user feedback, because it may take too long to run.
					//Console.WriteLine("Cycles processed: {0}", i);
				}
				Console.WriteLine("Patients processed: {0}", p + 1);
			}
		}

		static void ApplyMutationsProbabilities(int[,,] Matrix, int p, int i)
		{
			// This function will apply three probabilities: Deleterious, Beneficial or Neutral.
			// Their roles is to simulate real mutations of virus genome.
			// So here, there are mutational probabilities, which will bring an stochastic scenario sorting the progenies by the classes.

			int UpParticles = 0;
			int DownParticles = 0;

			// Here a random number greater than zero and less than one is selected. 
			Random rnd = new Random();
			double RandomNumber;
			//RandomNumber = rnd.NextDouble();
			//RandomNumber = 0.2;
			//RandomNumber = 0.903;

			// mutação deletéria = 90,0% de probabilidade (0,9)
			// mutação benéfica = 0,5% de probabilidade (0,005)
			// mutação neutra = 9,5% de probabilidade (0,095)
			// para efeitos de sorteio, qualquer número entre 0 e 0,9 será mutação deletéria
			// qualquer número entre 0,9 e 0,905 será mutação benéfica. 
			// Ou seja, o número sorteado precisa estar em um pequeno intervalo de 0,005 só que colocamos este intervalo acima de 0,9 
			// Qualquer número acima de 0,905 será mutação neutra
			// Não precisamos definir a mutação neutra, pois no código de comparação, o número sorteado deverá ser maior que 0,905 (deletéria + benéfica) 

			// Here the probabilities numbers for each mutation is defined.
			//double DeleteriousProbability = 0.6;
			//double BeneficialProbability = 0.005;

			int[] ThisCycle = new int[Class];

			for (int j = 0; j < Class; j++)
			{
				ThisCycle[j] = Matrix[p, i, j];
			}

			for (int j = 0; j < Class; j++)
			{
				if (ThisCycle[j] > 0 && i > 0)
				{
					for (int particles = ThisCycle[j]; particles > 0; particles--)
					{
						// In this loop, for each particle removed from the Matrix [i,j], a random number is selected.
						RandomNumber = rnd.NextDouble();

						// If the random number is less than the DeleteriousProbability defined, one particle of the previous Cycle will 
						// decrease one Class number. Remember this function is inside a loop for each i and each j values.
						// So this loop will run through the whole Matrix, particle by particle on its own positions. 

						if (RandomNumber < DeleteriousProbability[i])
						// Deleterious Mutation = 90,0% probability (0.9)
						{
							Matrix[p, i, (j - 1)] = Matrix[p, i, (j - 1)] + 1;
							Matrix[p, i, j] = Matrix[p, i, j] - 1;

							DownParticles++;
						}

						else if (RandomNumber < (DeleteriousProbability[i] + BeneficialProbability[i]))
						// Beneficial Mutation = 0,5% probability (0.005)
						{
							if (j < (Class - 1))
							{
								Matrix[p, i, (j + 1)] = Matrix[p, i, (j + 1)] + 1;
								Matrix[p, i, j] = Matrix[p, i, j] - 1;
							}
							if (j == Class)
							{
								Matrix[p, i, j] = Matrix[p, i, j] + 1;
							}

							UpParticles++;
						}
					}
				}
			}

			ClassUpParticles[p, i] = UpParticles;
			ClassDownParticles[p, i] = DownParticles;

			// PSEUDOCODIGO (para melhor compreensão no desenvolvimento):

			// se a classe R tiver partículas 
			// Para cada partícula da classe R, Ciclo n

			// Pensar numa régua de 0 a 1 (O número sorteado é de 0 a 1):
			// |____|____|____|____|____|____|____|____|____|____| 
			// 0   0.1                 0.5            0.8  0.9   1

			// MUTAÇÃO DELETÉRIA
			// Se o valor sorteado for menor que a probabilidade da mutação deletéria (valor sorteado menor ou igual a 0,8)
			// número de partículas da classe R recebe 1 partícula
			// número de partículas da classe (R + 1) perde uma partícula

			// MUTAÇÂO NEUTRA
			// Se o valor sorteado for maior do que a mutação deletéria, mas menor do que a mutação neutra, ou seja,
			// se o valor sorteado for maior do que 0.9 e menor do que 0.95
			// as partículas não se alteram.

			// MUTAÇÃO BENÉFICA
			// Se o valor sorteado for maior ou igual à probalidade da mutação neutra (valor sorteado maior ou igual à 0.95)
			// número de partículas da classe R perde 1 partícula
			// número de partículas da classe (R + 1) recebe uma partícula
		}

		static int ParticlesInCycle(int[,,] Matrix, int p, int i)
		{
			// This funtion brings the sum value of particles by Cycle. 

			int Particles = 0;

			for (int j = 0; j < Class; j++)
			{
				Particles = Particles + Matrix[p, i, j];
			}
			return Particles;
		}

		// PSEUDOCODIGO PARA SORTEIO E SELEÇÃO DE PARTÍCULAS PARA REDUÇÃO EM MAXPARTICLES POR CICLO (MÉTODO DIOGO)

		// Para cada ciclo: enquanto SOMALINHA > MAXPARTICLES
		// Sorteio de número (Sorteado) < SomaLinha

		// Sorteado é menor do que a quantidade de partículas em R0?
		// Se sim, tira uma partícula de R0; faz novo sorteio e recomeça o loop;
		// Se não, faz Sorteado menos a quantidade de partículas em R0, este é Sort1.

		// Sort1 é menor do que a quantidade de partículas em R1?
		// Se sim, tira uma partícula de R1; faz novo sorteio e recomeça o loop até cumprir com a condição;
		// Se não, faz Sort1 menos a quantidade de partículas em R2, este é Sort2.

		// Assim até quando necessário.

		// PSEUDOCODIGO PARA SORTEIO E SELEÇÃO DE PARTÍCULAS PARA REDUÇÃO EM MAXPARTICLES POR CICLO (MÉTODO MARCOS) = É o que será usado!!!

		// Faz um arrray (lista) ordenando as quantidades de partículas da seguinte forma (em um mesmo ciclo):
		// Array [0] = classe zero = quantidade de partículas na classe zero, ou seja, R0
		// Array [1] = quantidade de partículas em R0 + quantidade de partículas em R1;
		// Array [2] = quantidade de partículas em R0 + quantidade de partículas em R1 + quantidade de particulas em R2;
		// E assim por diante. Dessa forma, cada posição deste array poderá ter um valor máximo.

		// Para cada ciclo: enquanto SOMALINHA > MAXPARTICLES
		// Sorteio de número (Sorteado) < SomaLinha
		// Se o número sorteado for (0 < Sorteado <= Array[0]),
		// Matriz [Ciclo, 0] perderá uma partícula.

		// Assim vai até a SomaLinha chegar no MaxParticles determinado.

		static void CutOffMaxParticlesPerCycle(int[,,] Matrix, int p, int i, Random rndx)
		{
			int ParticlesInThisCycle = ParticlesInCycle(Matrix, p, i);  // Quantidade de partículas somadas por ciclo (linha)

			int[] StatusR = new int[Class];                             // Declarando o array que é a lista abaixo

			// Se, x = ParticlesInCycle, for maior do que o núm MaxParticles definido, então...
			if (ParticlesInThisCycle > MaxParticles)
			{
				// Para cada valor de x iniciando no valor de soma das partículas por ciclo;
				// sendo x, ou seja, esta soma, maior do que o limite MaxParticles definido;
				// então, diminua em uma unidade a soma das partículas por ciclo até que atinja o limite MaxParticles definido.

				for (int Particles = ParticlesInCycle(Matrix, p, i); Particles > MaxParticles; Particles--)
				// PARTICLES is equal to PARTICLESINTHISCYCLE, but we don't want to modifify PARTICLESINTHISCYCLE while the for loop is running
				// also, PARTICLESINTHISCYCLE was created outside the for loop, for other purpose
				{
					StatusR[0] = Matrix[p, i, 0];
					StatusR[1] = Matrix[p, i, 0] + Matrix[p, i, 1];
					StatusR[2] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2];
					StatusR[3] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3];
					StatusR[4] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4];
					StatusR[5] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5];
					StatusR[6] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6];
					StatusR[7] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7];
					StatusR[8] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8];
					StatusR[9] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9];
					StatusR[10] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9] + Matrix[p, i, 10];

					// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
					// int RandomMaxParticles;
					int rndParticle = rndx.Next(1, ParticlesInCycle(Matrix, p, i));

					// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
					// ParticlesInCycle atinja o limite estipulado por MaxParticles 
					if (rndParticle > 0 && rndParticle <= StatusR[0])
					{
						Matrix[p, i, 0] = Matrix[p, i, 0] - 1;
					}

					if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
					{
						Matrix[p, i, 1] = Matrix[p, i, 1] - 1;
					}

					if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
					{
						Matrix[p, i, 2] = Matrix[p, i, 2] - 1;
					}
					if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
					{
						Matrix[p, i, 3] = Matrix[p, i, 3] - 1;
					}
					if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
					{
						Matrix[p, i, 4] = Matrix[p, i, 4] - 1;
					}
					if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
					{
						Matrix[p, i, 5] = Matrix[p, i, 5] - 1;
					}
					if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
					{
						Matrix[p, i, 6] = Matrix[p, i, 6] - 1;
					}
					if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
					{
						Matrix[p, i, 7] = Matrix[p, i, 7] - 1;
					}
					if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
					{
						Matrix[p, i, 8] = Matrix[p, i, 8] - 1;
					}
					if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
					{
						Matrix[p, i, 9] = Matrix[p, i, 9] - 1;
					}
					if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
					{
						Matrix[p, i, 10] = Matrix[p, i, 10] - 1;
					}
				}
			}
		}

		static void PickRandomParticlesForInfection(int[,,] Matrix, int p, int i, Random rndx)
		{
			int InfectionParticles = 20;
			//int ParticlesSelected = 0;

			int ParticlesInThisCycle = ParticlesInCycle(Matrix, p, i);  // Quantidade de partículas somadas por ciclo (linha)

			int[] StatusR = new int[Class]; // TODO melhorar o nome deste array

			// TODO o FOR LOOP abaixo não utiliza todas as partículas disponíveis no ciclo
			// Em outras palavras, sobram partículas mesmo o ciclo tendo menos partículas do que INFECTIONPARTICLES

			//while (ParticlesSelected < InfectionParticles)
			//{
			//	StatusR[0] = Matrix[p, i, 0];
			//	StatusR[1] = Matrix[p, i, 0] + Matrix[p, i, 1];
			//	StatusR[2] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2];
			//	StatusR[3] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3];
			//	StatusR[4] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4];
			//	StatusR[5] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5];
			//	StatusR[6] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6];
			//	StatusR[7] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7];
			//	StatusR[8] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8];
			//	StatusR[9] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9];
			//	StatusR[10] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9] + Matrix[p, i, 10];

			//	// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
			//	// int RandomMaxParticles;
			//	if (ParticlesInThisCycle > 0)
			//	{
			//		int rndParticle = rndx.Next(1, ParticlesInThisCycle);

			//		// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
			//		// ParticlesInCycle atinja o limite estipulado por MaxParticles 
			//		if (rndParticle > 0 && rndParticle <= StatusR[0])
			//		{
			//			Matrix[(p + 1), 0, 0] += 1;
			//			Matrix[p, i, 0] -= 1;
			//			ParticlesSelected++;
			//		}

			//		if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
			//		{
			//			Matrix[(p + 1), 0, 1] += 1;
			//			Matrix[p, i, 1] -= 1;
			//			ParticlesSelected++;
			//		}

			//		if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
			//		{
			//			Matrix[(p + 1), 0, 2] += 1;
			//			Matrix[p, i, 2] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
			//		{
			//			Matrix[(p + 1), 0, 3] += 1;
			//			Matrix[p, i, 3] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
			//		{
			//			Matrix[(p + 1), 0, 4] += 1;
			//			Matrix[p, i, 4] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
			//		{
			//			Matrix[(p + 1), 0, 5] += 1;
			//			Matrix[p, i, 5] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
			//		{
			//			Matrix[(p + 1), 0, 6] += 1;
			//			Matrix[p, i, 6] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
			//		{
			//			Matrix[(p + 1), 0, 7] += 1;
			//			Matrix[p, i, 7] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
			//		{
			//			Matrix[(p + 1), 0, 8] += 1;
			//			Matrix[p, i, 8] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
			//		{
			//			Matrix[(p + 1), 0, 9] += 1;
			//			Matrix[p, i, 9] -= 1;
			//			ParticlesSelected++;
			//		}
			//		if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
			//		{
			//			Matrix[(p + 1), 0, 10] += 1;
			//			Matrix[p, i, 10] -= 1;
			//			ParticlesSelected++;
			//		}
			//	}
			//	else
			//	{
			//		Console.WriteLine("Generations {0} Cicle {1} has no particles. FOR LOOP iteration number {2}\t\t", p, i, ParticlesSelected);
			//		ParticlesSelected++;
			//	}
			//}

			for (int ParticlesSelected = 0; ParticlesSelected < InfectionParticles; ParticlesSelected++)
			{
				StatusR[0] = Matrix[p, i, 0];
				StatusR[1] = Matrix[p, i, 0] + Matrix[p, i, 1];
				StatusR[2] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2];
				StatusR[3] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3];
				StatusR[4] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4];
				StatusR[5] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5];
				StatusR[6] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6];
				StatusR[7] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7];
				StatusR[8] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8];
				StatusR[9] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9];
				StatusR[10] = Matrix[p, i, 0] + Matrix[p, i, 1] + Matrix[p, i, 2] + Matrix[p, i, 3] + Matrix[p, i, 4] + Matrix[p, i, 5] + Matrix[p, i, 6] + Matrix[p, i, 7] + Matrix[p, i, 8] + Matrix[p, i, 9] + Matrix[p, i, 10];

				// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
				// int RandomMaxParticles;
				if (ParticlesInThisCycle > 0)
				{
					int rndParticle = rndx.Next(1, ParticlesInThisCycle);

					// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
					// ParticlesInCycle atinja o limite estipulado por MaxParticles 
					if (rndParticle > 0 && rndParticle <= StatusR[0])
					{
						Matrix[(p + 1), 0, 0] += 1;
						Matrix[p, i, 0] -= 1;
					}

					if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
					{
						Matrix[(p + 1), 0, 1] += 1;
						Matrix[p, i, 1] -= 1;
					}

					if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
					{
						Matrix[(p + 1), 0, 2] += 1;
						Matrix[p, i, 2] -= 1;
					}
					if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
					{
						Matrix[(p + 1), 0, 3] += 1;
						Matrix[p, i, 3] -= 1;
					}
					if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
					{
						Matrix[(p + 1), 0, 4] += 1;
						Matrix[p, i, 4] -= 1;
					}
					if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
					{
						Matrix[(p + 1), 0, 5] += 1;
						Matrix[p, i, 5] -= 1;
					}
					if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
					{
						Matrix[(p + 1), 0, 6] += 1;
						Matrix[p, i, 6] -= 1;
					}
					if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
					{
						Matrix[(p + 1), 0, 7] += 1;
						Matrix[p, i, 7] -= 1;
					}
					if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
					{
						Matrix[(p + 1), 0, 8] += 1;
						Matrix[p, i, 8] -= 1;
					}
					if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
					{
						Matrix[(p + 1), 0, 9] += 1;
						Matrix[p, i, 9] -= 1;
					}
					if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
					{
						Matrix[(p + 1), 0, 10] += 1;
						Matrix[p, i, 10] -= 1;
					}
				}
				else
				{
					Console.WriteLine("Generations {0} Cicle {1} has no particles. FOR LOOP iteration number {2}\t\t", p, i, ParticlesSelected);
				}
			}
		}

		static void PrintOutput(int[,,] Matrix)
		{
			double PercentageOfParticlesUp = 0.0;
			double PercentageOfParticlesDown = 0.0;

			StreamWriter writer = new StreamWriter("numbers.txt");
			// The writer will bring the output file (txt in this case)
			// Ensure the writer will be closed when no longer used
			using (writer)
			{
				// Formatting Output for the Console screen. 
				Console.WriteLine("");
				Console.Write("\t\t\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\tR9\t\tR10\n\n");
				writer.Write("\t\tSoma\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\t\tR9\t\tR10\n\n");
				writer.WriteLine("\n");

				for (int p = 0; p < Generations; p++)
				{
					for (int i = 0; i < Cycle; i++)
					{
						Console.Write("Gen.{0} Cic.{1}\t\t", p, i);
						writer.Write("Gen.{0} Cic.{1} {2}\t\t", p, i, ParticlesInCycle(Matrix, p, i));

						for (int j = 0; j < Class; j++)
						{
							Console.Write("{0}\t", Matrix[p, i, j]);
							writer.Write("{0}\t", Matrix[p, i, j]);
						}

						PercentageOfParticlesUp = (Convert.ToDouble(ClassUpParticles[p, i]) / Convert.ToDouble(ParticlesInCycle(Matrix, p, i))) * 100;
						PercentageOfParticlesDown = (Convert.ToDouble(ClassDownParticles[p, i]) / Convert.ToDouble(ParticlesInCycle(Matrix, p, i))) * 100;

						Console.WriteLine("\nSoma do ciclo {0}: {1}", i, ParticlesInCycle(Matrix, p, i));
						Console.WriteLine("Particles Up: {0}, {1} %", ClassUpParticles[p, i], PercentageOfParticlesUp);
						Console.WriteLine("Particles Down: {0}, {1} %", ClassDownParticles[p, i], PercentageOfParticlesDown);
						Console.Write("\n");

						writer.WriteLine("\n");
					}

					Console.WriteLine("***************************************************************************************************************");
					Console.Write("\n");
					Console.Write("\n");
				}
			}
		}
	}
}
