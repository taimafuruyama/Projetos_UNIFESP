using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics; // used for the Stopwatch Class
using System.Threading; // used for the Stopwatch Class

// TODO aumentar poder dos valores = números maiores (double por exemplo - maior e mais preciso).
// TODO limite de partículas por ciclo
// TODO fazer mutação benéfica e neutra com probabilidade fixa
// TODO fazer mutações com probabilidades aleatórias
// TODO *** avaliar quando encerrar um paciente e passar para o próximo (média das classes for constante)
// TODO fazer mais de um paciente
// TODO fazer simulação definindo em quais ciclos ocorrem infecções e deixar pacientes inicais rodando
// TODO interface gráfica (gráficos em tempo real, novas janelas para cada paciente etc)

// TODO: A INTRO explanation about this program, the main use, the aim, how it works, the output and what to do with.


namespace multi_dimensional_array
{
	public class Program
	{
		// create and start the Stopwatch Class. See: https://msdn.microsoft.com/en-us/library/system.diagnostics.stopwatch
		Stopwatch ProgramTimer = new Stopwatch();
		ProgramTimer.Start();
		
		// Definition of Cycle
		public const int Cycle = 10;

		// Definition of Class
		public const int Class = 11;

		// Definition of Patient
		public const int Patient = 0;

		// The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
		public const int InitialParticles = 5;

		static void Main(string[] args)
		{
			// Declaring the two-dimensional Matrix: it has x lines of Cycles and y columns of Classes, defined by the variables above. 
			int[,] Matrix = new int[Cycle, Class];
			//int[,] TempMatrix = new int[Cycle, Class];

			// The Matrix starts on the 10th position (column) on the line zero. 
			// The "InitialParticles" is the amount of viral particles that exists in the class 10 on the cycle zero.
			// That is: these 5 particles have the potential to create 10 particles each.
			Matrix[0, 10] = InitialParticles;
			
			// TODO put the for loop below inside a function called, for example POPULATEMATRIX, 
			// because the main fucntion is getting too big again

			// Main Loop to create more particles on the next Cycles from the Cycle Zero (lines values).
			// Each matrix position will bring a value. This value will be mutiplied by its own class number (column value).  
			for (int i = 0; i < Cycle; i++)
			{
				for (int j = 0; j < Class; j++)
				{
					if (i > 0)
					{
						// Multiplies the number os particles from de previous Cycle by the Class number which belongs.
						// This is the progeny composition.
						Matrix[i, j] = Matrix[(i - 1), j] * j;

						//Matrix[i, j] = TempMatrix[i, j];
						//Matrix[i, j] = 0;

					}
					CutOffMaxParticlesPerCicle(Matrix, i);
					ApplyMutationsProbabilities(Matrix, i, j);
				}
				// print which Cycle was finished just to give a user feedback, because it was taking too long to run.
				Console.WriteLine("Cycles processed: {0}", i);
			}
			ProgramTimer.Stop();
			PrintOutput(Matrix);
			
			// Get the elapsed time as a TimeSpan value.
			TimeSpan ts = ProgramTimer.Elapsed;

			// Format and display the TimeSpan value.
			string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);
			Console.WriteLine("Total Run Time: " + elapsedTime);
		}

		static void ApplyMutationsProbabilities(int[,] Matrix, int i, int j)
		{
			// This function will apply three probabilities: Deleterious, Beneficial or Neutral.
			// Their roles is to simulate real mutations of virus genome.
			// So here, there are mutational probabilities, which will bring an stochastic scenario sorting the progenies by the classes.

			// Here a random number greater than zero and less than one is selected. 
			Random rnd = new Random();      // !!! ATENÇÃO: Cuidado para não chamar mais de uma vez e dar dois números aleatorios iguais
			double RandomNumber;
			//RandomNumber = rnd.NextDouble();
			//RandomNumber = 0.2;
			
			// mutação deletéria = 90,0% de probabilidade (0,9)
			// mutação benéfica = 0,5% de probabilidade (0,005)
			// mutação neutra = 9,5% de probabilidade (0,095)

			// para efeitos de sorteio, qualquer número entre 0 e 0,9 será mutação deletéria
			// qualquer número acima de 0,995 será mutação benéfica. Ou seja, o número sorteado precisa estar em um 
			// pequeno intervalo de 0,005 só que colocamos este intervalo na parte superior do intervalo entre 0 e 1
			// e qualquer número entre 0,9 e 0,995 será mutação neutra. Não precisamos definir a mutação neutra, 
			// pois no código de comparação, o número sorteado deverá ser maior que 0,9 (deletéria) e menor que 
			// 0,995 (benéfica)

			double DeleteriousProbability = 0.9;
			double BeneficialProbability = 1 - 0,005; // ou, 0,995

			if (Matrix[i, j] > 0)
			{
				for (int x = Matrix[i, j]; x > 0; x--)
				{
					// Inside this loop, for each particle removed from the Matrix [i,j], a random number is selected.
					RandomNumber = rnd.NextDouble();

					// If the random number is less than the DeleteriousProbability defined, one particle of the previous Cycle will 
					// decrease one Class number. Remember this function is inside a loop for each i and each j values.
					// So this loop will run through the whole Matrix, particle by particle on its own positions. 

					// Deletéria: Random menor ou igual do que 0.8
					if (RandomNumber <= DeleteriousProbability)		
					{
						if (i > 0)
						{
							//Matrix[(i - 1), j]++;
							//TempMatrix[i, j]--;

							Matrix[i, (j - 1)] = Matrix[i, (j - 1)] + 1;
							Matrix[i, j] = Matrix[i, j] - 1;
						}
					}

					// Neutra: Random maior do que 0.8, menor do que 0.95
					if (RandomNumber > DeleteriousProbability && RandomNumber < BeneficialProbability)
					{
						Matrix[i, j] = Matrix[i, j];
					}

					// Benéfica: maior ou igual à neutra
					if (RandomNumber >= BeneficialProbability)
					{
						if (i > 0)
						{
							if (j < (Class - 1)) 
							{
								Matrix[i, (j + 1)] = Matrix[i, (j + 1)] + 1;
								Matrix[i, j] = Matrix[i, j] - 1;
							}
							if (j == Class)
							{
								Matrix[i, j] = Matrix[i, j] + 1;
							}
						}
					}
				}
			}

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

		static int ParticlesInCycle(int[,] Matrix, int i)
		{
			// This funtion brings the sum value of particles by Cycle. 

			int Particles = 0;

			for (int j = 0; j < Class; j++)
			{
				Particles = Particles + Matrix[i, j];
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

		static void CutOffMaxParticlesPerCicle(int[,] Matrix, int i)
		{
			int MaxParticles = 1000000;								   // Limite máximo de partículas que quero impor para cada ciclo (linha)
			int ParticlesInThisCycle = ParticlesInCycle(Matrix, i);	   // Quantidade de partículas somadas por ciclo (linha)

			int[] StatusR = new int[Class];							   // Declarando o array que é a lista abaixo
			StatusR[0] = Matrix[i, 0];
			StatusR[1] = Matrix[i, 0] + Matrix[i, 1];
			StatusR[2] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2];
			StatusR[3] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3];
			StatusR[4] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4];
			StatusR[5] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5];
			StatusR[6] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5] + Matrix[i, 6];
			StatusR[7] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5] + Matrix[i, 6] + Matrix[i, 7];
			StatusR[8] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5] + Matrix[i, 6] + Matrix[i, 7] + Matrix[i, 8];
			StatusR[9] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5] + Matrix[i, 6] + Matrix[i, 7] + Matrix[i, 8] + Matrix[i, 9];
			StatusR[10] = Matrix[i, 0] + Matrix[i, 1] + Matrix[i, 2] + Matrix[i, 3] + Matrix[i, 4] + Matrix[i, 5] + Matrix[i, 6] + Matrix[i, 7] + Matrix[i, 8] + Matrix[i, 9] + Matrix[i, 10];

			// Se, x = ParticlesInCycle, for maior do que o núm MaxParticles definido, então...
			if (ParticlesInThisCycle > MaxParticles)
			{
				// Para cada valor de x iniciando no valor de soma das partículas por ciclo;
				// sendo x, ou seja, esta soma, maior do que o limite MaxParticles definido;
				// então, diminua em uma unidade a soma das partículas por ciclo até que atinja o limite MaxParticles definido.

				for (int Particles = ParticlesInCycle(Matrix, i); Particles > MaxParticles; Particles--)
				// PARTICLES is equal to PARTICLESINTHISCYCLE, but we don't want to modifify PARTICLESINTHISCYCLE while the for loop is running
				// also, PARTICLESINTHISCYCLE was created outside the for loop, for other purpose
				{
					// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
					// int RandomMaxParticles;
					Random rndx = new Random();
					int rndParticle = rndx.Next(1, ParticlesInCycle(Matrix, i));

					// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
					// ParticlesInCycle atinja o limite estipulado por MaxParticles 
					if (rndParticle > 0 && rndParticle <= StatusR[0])
					{
						Matrix[i, 0] = Matrix[i, 0] - 1;
					}

					if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
					{
						Matrix[i, 1] = Matrix[i, 1] - 1;
					}

					if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
					{
						Matrix[i, 2] = Matrix[i, 2] - 1;
					}
					if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
					{
						Matrix[i, 3] = Matrix[i, 3] - 1;
					}
					if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
					{
						Matrix[i, 4] = Matrix[i, 4] - 1;
					}
					if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
					{
						Matrix[i, 5] = Matrix[i, 5] - 1;
					}
					if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
					{
						Matrix[i, 6] = Matrix[i, 6] - 1;
					}
					if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
					{
						Matrix[i, 7] = Matrix[i, 7] - 1;
					}
					if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
					{
						Matrix[i, 8] = Matrix[i, 8] - 1;
					}
					if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
					{
						Matrix[i, 9] = Matrix[i, 9] - 1;
					}
					if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
					{
						Matrix[i, 10] = Matrix[i, 10] - 1;
					}
				}
			}
		}


		static void PrintOutput(int[,] Matrix)
		{
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

				// Outer loop for accessing rows
				for (int i = 0; i < Cycle; i++)
				{
					Console.Write("Pac.{0} Cic.{1}\t\t", Patient, i);
					writer.Write("Pac.{0} Cic.{1} {2}\t\t", Patient, i, ParticlesInCycle(Matrix, i));

					// Inner or nested loop for accessing column of each row
					for (int j = 0; j < Class; j++)
					{
						Console.Write("{0}\t", Matrix[i, j]);
						writer.Write("{0}\t", Matrix[i, j]);
					}

					Console.WriteLine("\nSoma do ciclo {0}: {1}", i, ParticlesInCycle(Matrix, i));
					Console.Write("\n");
					writer.WriteLine("\n");
				}
				Console.ReadLine();
			}
		}
	}
}
