#include <iostream>
#include <fstream>
#include <array>
#include <numeric>
#include <vector>
#include <algorithm>
#include <cmath>

#define N 150
#define MAX_IT 300
#define MIN_I 200
#define T_MODIFIER 1e-4

void print_array(std::array<std::array<int, 2>, N>);

template <typename T>
void print_vector(std::vector<T> vec) {
  std::cout << std::endl;
  for (const auto& element : vec) {
    std::cout << element << ", ";
  }
  std::cout << vec[0] << std::endl;
}

double get_distance(const std::array<std::array<int, 2>, N>&, const std::vector<uint32_t>&);

void swap_edges(uint32_t, uint32_t, std::vector<uint32_t>&);

void save_to_file(const std::string&, const std::array<std::array<int, 2>, N>&, const std::vector<uint32_t>&, double);

std::vector<uint32_t> simulated_annealing(const std::string&, const std::string&, const std::array<std::array<int, 2>, N>&);