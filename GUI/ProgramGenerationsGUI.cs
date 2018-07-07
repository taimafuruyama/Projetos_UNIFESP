using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Windows.Forms;

namespace ProgramGenerationsGUI
{
	public partial class ProgramGenerationsGUI : Form
	{
		public ProgramGenerationsGUI()
		{
			InitializeComponent();

			// Number of Generations
			// Generation 0 always have only 1 patient
			// Generations 1 and forward have the number of patients defined in the PATIENTS variable
			int Generations = 2;

			// this array is called inside the RunPatients function
			// it is an array because if there is increment from the infection cycle from one patient to another,
			// different values for infection cycle have to be stored
			int[] InfectionCycle = new int[] { 2, 4 };

			// Number of Patients in Generation 1
			int Gen1Patients;

			// Number of Cycles
			int Cycles = 10;

			// Number of Classes
			int Classes = 11;

			// The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
			int InitialParticles = 5;

			int InfectionParticles = 20;
	
			int MaxParticles = 1000000; // Limite máximo de partículas que quero impor para cada ciclo (linha)

			double[] DeleteriousProbability = new double[Cycles];
			double[] BeneficialProbability = new double[Cycles];

			bool BeneficialIncrement = false; // if true, beneficial probability will increase by INCREMENT each cycle
														   // if false, it will change from a fixed value to another fixed value, at the chosen cycle
			bool DeleteriousIncrement = false; // if true, deleterious probability will increase by INCREMENT each cycle
														// if false, it will change from a fixed value to another fixed value, at the chosen cycle

			// Lists to keep the number of particles that go up or down the classes, during mutations
			int[][,] ClassUpParticles = new int[Generations][,];
			int[][,] ClassDownParticles = new int[Generations][,];

			MainFunction();

			void MainFunction()
			{
				Random rnd = new Random();

				// number of patients at 1st generation is defined by the number of cycles that 
				// occur infection
				Gen1Patients = InfectionCycle.GetLength(0);

				// create and start the Stopwatch Class. From: https://msdn.microsoft.com/en-us/library/system.diagnostics.stopwatch
				Stopwatch stopWatch = new Stopwatch();
				stopWatch.Start();
				//Thread.Sleep(10000);

				// Declaring the three-dimensional Matrix: it has p Patient, x lines of Cycles and y columns of Classes, defined by the variables above. 

				int[][,,] Matrix = new int[Generations][,,];

				for (int g = 0; g < Generations; g++)
				{
					Matrix[g] = new int[(int)Math.Pow(Gen1Patients, g), Cycles, Classes];
					//InfectionCycle[g] = new int[(int)Math.Pow(Gen1Patients, g)];
					ClassUpParticles[g] = new int[(int)Math.Pow(Gen1Patients, g), Cycles];
					ClassDownParticles[g] = new int[(int)Math.Pow(Gen1Patients, g), Cycles];
				}

				//FillInfectionCycleArray(6, 0); // FIRST PARAMETER: initial cycle, SECOND PARAMENTER: increment

				if (DeleteriousIncrement)
				{
					FillDeleteriousArrayWithIncrement(0.3, 0.1); // FIRST PARAMETER: initial probability, SECOND PARAMENTER: increment
				}
				else
				{
					FillDeleteriousArray(0.8, 0.9, 5); // FIRST PARAMETER: first probability, SECOND PARAMENTER: second probability
													   // THIRD PARAMETER: cycle to change from first probability to second probability
				}

				if (BeneficialIncrement)
				{
					FillBeneficialArrayWithIncrement(0.0003, 0.0001); // FIRST PARAMETER: initial probability, SECOND PARAMENTER: increment
				}
				else
				{
					FillBeneficialArray(0.0003, 0.0008, 5); // FIRST PARAMETER: first probability, SECOND PARAMENTER: second probability
															// THIRD PARAMETER: cycle to change from first probability to second probability
				}

				// The Matrix starts on the Patient 0, 10th position (column) on the line zero. 
				// The "InitialParticles" is the amount of viral particles that exists in the class 10 on the cycle zero.
				// That is: these 5 particles have the potential to create 10 particles each.

				Matrix[0][0, 0, 10] = InitialParticles;

				RunPatients(Matrix, rnd);

				stopWatch.Stop();
				// Get the elapsed time as a TimeSpan value.
				TimeSpan ts = stopWatch.Elapsed;

				PrintOutput(Matrix);

				// Format and display the TimeSpan value.
				string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);
				OutputConsole.AppendText(Environment.NewLine);
				OutputConsole.AppendText("Total Run Time: " + elapsedTime);

			}

			void FillDeleteriousArray(double FirstProbability, double SecondProbability, int ChangeCycle)
			{
				for (int i = 0; i < DeleteriousProbability.GetLength(0); i++)
				{
					if (i <= ChangeCycle)
					{
						DeleteriousProbability[i] = FirstProbability;
					}
					else
					{
						DeleteriousProbability[i] = SecondProbability;
					}
				}
			}

			void FillDeleteriousArrayWithIncrement(double InitialProbability, double Increment)
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

			void FillBeneficialArray(double FirstProbability, double SecondProbability, int ChangeCycle)
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

			void FillBeneficialArrayWithIncrement(double InitialProbability, double Increment)
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

			void RunPatients(int[][,,] Matrix, Random rndx)
			{
				// Main Loop to create more particles on the next Cycles from the Cycle Zero (lines values).
				// Each matrix position will bring a value. This value will be mutiplied by its own class number (column value). 
				for (int g = 0; g < Generations; g++)
				{
					for (int p = 0; p < Matrix[g].GetLength(0); p++)
					{
						Console.WriteLine("Patient started: GEN {0} - P {1}", g, p);

						for (int i = 0; i < Cycles; i++)
						{
							for (int j = 0; j < Classes; j++)
							{
								if (i > 0)
								{
									// Multiplies the number os particles from de previous Cycle by the Class number which belongs.
									// This is the progeny composition.
									//Matrix[p, i, j] = Matrix[p, (i - 1), j] * j;
									Matrix[g][p, i, j] = Matrix[g][p, (i - 1), j] * j;
								}
							}

							CutOffMaxParticlesPerCycle(Matrix, g, p, i, rndx);
							ApplyMutationsProbabilities(Matrix, g, p, i);

							// if the INFECTIONCYLE array contains the cycle "i"
							// and it is not the last generation, make infection
							if (InfectionCycle.Contains(i) && (g < Generations - 1))
							{
								PickRandomParticlesForInfection(Matrix, g, p, i, rndx);
								//Console.WriteLine("*** INFECTION CYCLE *** {0}", i);
							}

							// print which Cycle was finished just to give user feedback, because it may take too long to run.
							//Console.WriteLine("Cycles processed: {0}", i);
						}
						//Console.WriteLine("Patients processed: GEN {0} - P {1}", g, p);
					}
				}
			}

			void ApplyMutationsProbabilities(int[][,,] Matrix, int g, int p, int i)
			{
				// This function will apply three probabilities: Deleterious, Beneficial or Neutral.
				// Their roles is to simulate real mutations of virus genome.
				// So here, there are mutational probabilities, which will bring an stochastic scenario sorting the progenies by the classes.

				int UpParticles = 0;
				int DownParticles = 0;

				// Here a random number greater than zero and less than one is selected. 
				Random rnd = new Random();
				double RandomNumber;

				// array to store the number of particles of each class, in the current cycle
				int[] ThisCycle = new int[Classes];

				for (int j = 0; j < Classes; j++)
				{
					// storing the number of particles of each class (j)
					ThisCycle[j] = Matrix[g][p, i, j];
				}

				for (int j = 0; j < Classes; j++)
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
								Matrix[g][p, i, (j - 1)] = Matrix[g][p, i, (j - 1)] + 1;
								Matrix[g][p, i, j] = Matrix[g][p, i, j] - 1;

								DownParticles++;
							}

							else if (RandomNumber < (DeleteriousProbability[i] + BeneficialProbability[i]))
							// Beneficial Mutation = 0,5% probability (0.005)
							{
								if (j < (Classes - 1))
								{
									Matrix[g][p, i, (j + 1)] = Matrix[g][p, i, (j + 1)] + 1;
									Matrix[g][p, i, j] = Matrix[g][p, i, j] - 1;
								}
								if (j == Classes)
								{
									Matrix[g][p, i, j] = Matrix[g][p, i, j] + 1;
								}

								UpParticles++;
							}
						}
					}
				}
				ClassUpParticles[g][p, i] = UpParticles;
				ClassDownParticles[g][p, i] = DownParticles;
			}

			int ParticlesInCycle(int[][,,] Matrix, int g, int p, int i)
			{
				// This funtion brings the sum value of particles by Cycle. 

				int Particles = 0;

				for (int j = 0; j < Classes; j++)
				{
					Particles = Particles + Matrix[g][p, i, j];
				}
				return Particles;
			}

			void CutOffMaxParticlesPerCycle(int[][,,] Matrix, int g, int p, int i, Random rndx)
			{
				int ParticlesInThisCycle = ParticlesInCycle(Matrix, g, p, i);  // Quantidade de partículas somadas por ciclo (linha)

				int[] StatusR = new int[Classes];                             // Declarando o array que é a lista abaixo

				// Se, x = ParticlesInCycle, for maior do que o núm MaxParticles definido, então...
				if (ParticlesInThisCycle > MaxParticles)
				{
					// Para cada valor de x iniciando no valor de soma das partículas por ciclo;
					// sendo x, ou seja, esta soma, maior do que o limite MaxParticles definido;
					// então, diminua em uma unidade a soma das partículas por ciclo até que atinja o limite MaxParticles definido.

					for (int Particles = ParticlesInCycle(Matrix, g, p, i); Particles > MaxParticles; Particles--)
					// PARTICLES is equal to PARTICLESINTHISCYCLE, but we don't want to modifify PARTICLESINTHISCYCLE while the for loop is running
					// also, PARTICLESINTHISCYCLE was created outside the for loop, for other purpose
					{
						StatusR[0] = Matrix[g][p, i, 0];
						StatusR[1] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1];
						StatusR[2] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2];
						StatusR[3] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3];
						StatusR[4] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4];
						StatusR[5] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5];
						StatusR[6] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6];
						StatusR[7] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7];
						StatusR[8] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8];
						StatusR[9] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8] + Matrix[g][p, i, 9];
						StatusR[10] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8] + Matrix[g][p, i, 9] + Matrix[g][p, i, 10];

						// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
						// int RandomMaxParticles;
						int rndParticle = rndx.Next(1, ParticlesInCycle(Matrix, g, p, i));

						// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
						// ParticlesInCycle atinja o limite estipulado por MaxParticles 
						if (rndParticle > 0 && rndParticle <= StatusR[0])
						{
							Matrix[g][p, i, 0] = Matrix[g][p, i, 0] - 1;
						}

						if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
						{
							Matrix[g][p, i, 1] = Matrix[g][p, i, 1] - 1;
						}

						if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
						{
							Matrix[g][p, i, 2] = Matrix[g][p, i, 2] - 1;
						}
						if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
						{
							Matrix[g][p, i, 3] = Matrix[g][p, i, 3] - 1;
						}
						if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
						{
							Matrix[g][p, i, 4] = Matrix[g][p, i, 4] - 1;
						}
						if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
						{
							Matrix[g][p, i, 5] = Matrix[g][p, i, 5] - 1;
						}
						if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
						{
							Matrix[g][p, i, 6] = Matrix[g][p, i, 6] - 1;
						}
						if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
						{
							Matrix[g][p, i, 7] = Matrix[g][p, i, 7] - 1;
						}
						if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
						{
							Matrix[g][p, i, 8] = Matrix[g][p, i, 8] - 1;
						}
						if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
						{
							Matrix[g][p, i, 9] = Matrix[g][p, i, 9] - 1;
						}
						if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
						{
							Matrix[g][p, i, 10] = Matrix[g][p, i, 10] - 1;
						}
					}
				}
			}

			void PickRandomParticlesForInfection(int[][,,] Matrix, int g, int p, int i, Random rndx)
			{
				bool NoParticlesForInfection = false;

				// array to store the particles that will infect patients of the next generation
				// it is just a 1D array (a list) where each index is a class
				int[] InfectedParticles = new int[Classes];

				int ParticlesInThisCycle = ParticlesInCycle(Matrix, g, p, i);  // Quantidade de partículas somadas por ciclo (linha)

				int[] StatusR = new int[Classes]; // TODO melhorar o nome deste array

				for (int ParticlesSelected = 0; ParticlesSelected < InfectionParticles; ParticlesSelected++)
				{
					StatusR[0] = Matrix[g][p, i, 0];
					StatusR[1] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1];
					StatusR[2] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2];
					StatusR[3] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3];
					StatusR[4] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4];
					StatusR[5] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5];
					StatusR[6] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6];
					StatusR[7] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7];
					StatusR[8] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8];
					StatusR[9] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8] + Matrix[g][p, i, 9];
					StatusR[10] = Matrix[g][p, i, 0] + Matrix[g][p, i, 1] + Matrix[g][p, i, 2] + Matrix[g][p, i, 3] + Matrix[g][p, i, 4] + Matrix[g][p, i, 5] + Matrix[g][p, i, 6] + Matrix[g][p, i, 7] + Matrix[g][p, i, 8] + Matrix[g][p, i, 9] + Matrix[g][p, i, 10];

					// Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
					// int RandomMaxParticles;
					if (ParticlesInThisCycle > 0)
					{
						int rndParticle = rndx.Next(1, ParticlesInThisCycle);

						// Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
						// ParticlesSelected atinja o limite estipulado por InfectioParticles 
						if (rndParticle > 0 && rndParticle <= StatusR[0])
						{
							InfectedParticles[0] += 1;
							Matrix[g][p, i, 0] -= 1;
						}

						if (rndParticle > StatusR[0] && rndParticle <= StatusR[1])
						{
							InfectedParticles[1] += 1;
							Matrix[g][p, i, 1] -= 1;
						}

						if (rndParticle > StatusR[1] && rndParticle <= StatusR[2])
						{
							InfectedParticles[2] += 1;
							Matrix[g][p, i, 2] -= 1;
						}
						if (rndParticle > StatusR[2] && rndParticle <= StatusR[3])
						{
							InfectedParticles[3] += 1;
							Matrix[g][p, i, 3] -= 1;
						}
						if (rndParticle > StatusR[3] && rndParticle <= StatusR[4])
						{
							InfectedParticles[4] += 1;
							Matrix[g][p, i, 4] -= 1;
						}
						if (rndParticle > StatusR[4] && rndParticle <= StatusR[5])
						{
							InfectedParticles[5] += 1;
							Matrix[g][p, i, 5] -= 1;
						}
						if (rndParticle > StatusR[5] && rndParticle <= StatusR[6])
						{
							InfectedParticles[6] += 1;
							Matrix[g][p, i, 6] -= 1;
						}
						if (rndParticle > StatusR[6] && rndParticle <= StatusR[7])
						{
							InfectedParticles[7] += 1;
							Matrix[g][p, i, 7] -= 1;
						}
						if (rndParticle > StatusR[7] && rndParticle <= StatusR[8])
						{
							InfectedParticles[8] += 1;
							Matrix[g][p, i, 8] -= 1;
						}
						if (rndParticle > StatusR[8] && rndParticle <= StatusR[9])
						{
							InfectedParticles[9] += 1;
							Matrix[g][p, i, 9] -= 1;
						}
						if (rndParticle > StatusR[9] && rndParticle <= StatusR[10])
						{
							InfectedParticles[10] += 1;
							Matrix[g][p, i, 10] -= 1;
						}
					}
					else
					{
						NoParticlesForInfection = true;
					}
				}

				// if there are no particles for infection, there is no infection
				if (NoParticlesForInfection)
				{
					Console.WriteLine("Patient {0} Cycle {1} has no particles.\t\t", p, i);
				}
				else
				{
					InfectPatients(Matrix, InfectedParticles, g, p, i, rndx);
				}
			}

			void InfectPatients(int[][,,] Matrix, int[] InfectedParticles, int g, int p, int i, Random rndx)
			{
				int AmountOfParticlesAvailable = InfectedParticles[0] + InfectedParticles[1] + InfectedParticles[2] + InfectedParticles[3] +
							InfectedParticles[4] + InfectedParticles[5] + InfectedParticles[6] + InfectedParticles[7] +
							InfectedParticles[8] + InfectedParticles[9] + InfectedParticles[10];

				//Console.WriteLine(AmountOfParticlesAvailable);

				int[] PatientsToInfect = new int[Gen1Patients];

				// each patient will infect a group of patients of size Gen1Patients
				int LastPatient = ((p + 1) * Gen1Patients) - 1; // the last patient of this group
				int FirstPatient = LastPatient - (Gen1Patients - 1); // the first patient of this group

				for (int x = 0; x < Gen1Patients; x++)
				{
					PatientsToInfect[x] = FirstPatient + x;
					//Console.WriteLine(PatientsToInfect[x]);
				}

				//Console.WriteLine(FirstPatient);
				//Console.WriteLine(LastPatient);

				int patient = PatientsToInfect[Array.IndexOf(InfectionCycle, i)];

				while (AmountOfParticlesAvailable > 0)
				{
					int rndClass = rndx.Next(0, Classes);

					if (InfectedParticles[rndClass] > 0) // there is at least one particle in the class selected
					{
						Matrix[g + 1][patient, 0, rndClass] += 1;
						//ParticlesReceived[patient] += 1;
						InfectedParticles[rndClass] -= 1;
						AmountOfParticlesAvailable--;
					}
				}

				Console.WriteLine("G {0} P {1} infected G {2} P {3}", g, p, g + 1, patient);
			}

			void PrintOutput(int[][,,] Matrix)
			{
				double PercentageOfParticlesUp = 0.0;
				double PercentageOfParticlesDown = 0.0;

				//StreamWriter writer = new StreamWriter("numbers.txt");
				// The writer will bring the output file (txt in this case)
				// Ensure the writer will be closed when no longer used
				//using (writer)
				{
					// Formatting Output for the Console screen. 
					OutputConsole.AppendText("\t\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\tR9\tR10");
					OutputConsole.AppendText(Environment.NewLine);
					OutputConsole.AppendText(Environment.NewLine);
					//writer.Write("\t\tSoma\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\t\tR9\t\tR10\n\n");
					//writer.WriteLine("\n");

					for (int g = 0; g < Generations; g++)
					{
						for (int p = 0; p < Matrix[g].GetLength(0); p++)
						{
							for (int i = 0; i < Cycles; i++)
							{
								OutputConsole.AppendText("G " + g + " P " + p + " Cycle " + i + "\t");
								//writer.Write("G {0} P {1} Cic.{2} {3}\t\t", g, p, i, ParticlesInCycle(Matrix, g, p, i));

								for (int j = 0; j < Classes; j++)
								{
									OutputConsole.AppendText(Matrix[g][p, i, j].ToString() + "\t");
									//writer.Write("{0}\t", Matrix[g][p, i, j]);
								}

								PercentageOfParticlesUp = (Convert.ToDouble(ClassUpParticles[g][p, i]) / Convert.ToDouble(ParticlesInCycle(Matrix, g, p, i))) * 100;
								PercentageOfParticlesDown = (Convert.ToDouble(ClassDownParticles[g][p, i]) / Convert.ToDouble(ParticlesInCycle(Matrix, g, p, i))) * 100;

								Console.WriteLine("\nSoma do ciclo {0}: {1}", i, ParticlesInCycle(Matrix, g, p, i));
								Console.WriteLine("Particles Up: {0}, {1} %", ClassUpParticles[g][p, i], PercentageOfParticlesUp);
								Console.WriteLine("Particles Down: {0}, {1} %", ClassDownParticles[g][p, i], PercentageOfParticlesDown);
								Console.Write("\n");

								OutputConsole.AppendText(Environment.NewLine);
								OutputConsole.AppendText(Environment.NewLine);
								//writer.WriteLine("\n");
							}
							OutputConsole.AppendText("******************************************************" +
								"*************************************************************************************************");
							OutputConsole.AppendText(Environment.NewLine);
						}
					}
				}
			}
		}
	}	
}

