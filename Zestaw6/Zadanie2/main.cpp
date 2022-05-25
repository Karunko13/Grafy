#include "functions.h"

/* To change MIN_I, MAX_IT and N, go into functions.h file */

int main(int argc, char const *argv[])
{
  srand(time(NULL));
  std::array<std::array<int, 2>, N> data_arr;
  int value = 0;
  std::ifstream data("input_150.dat");
  uint32_t pos = 0;
  while (data) {
    data >> value;
    if (data) {
      data_arr[pos/2][pos%2] = value;
      pos++;
    } else {
      break;
    }
  }
  data.close();
  for (int i = 0; i < 20; i++) {
    // simulated_annealing("linear", std::to_string(i), data_arr);
    simulated_annealing("square", std::to_string(i), data_arr);
  }
  
  return 0;
}

