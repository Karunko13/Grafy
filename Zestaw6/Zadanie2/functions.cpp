#include "functions.h"

void print_array(std::array<std::array<int, 2>, N> arr) {
  for (const auto& row: arr) {
    for (const auto& elem: row) {
      std::cout << elem << ' ';
    }
    std::cout << std::endl;
  }
}

double get_distance(const std::array<std::array<int, 2>, N>& nodes, const std::vector<uint32_t>& cycle) {
  double sum = 0;
  uint32_t previous_node = cycle[0];
  for (const uint32_t& current_node: cycle) {
    sum += sqrt(pow(nodes[current_node][1] - nodes[previous_node][1], 2) + pow(nodes[current_node][0] - nodes[previous_node][0], 2));
    previous_node = current_node;
  }
  return sum + sqrt(pow(nodes[cycle[0]][1] - nodes[previous_node][1], 2) + pow(nodes[cycle[0]][0] - nodes[previous_node][0], 2));
}

void swap_edges(uint32_t ab, uint32_t cd, std::vector<uint32_t>& cycle) {
  uint32_t tmp;
  if (cd < ab) {
    tmp = ab;
    ab = cd;
    cd = tmp;
  }

  for(uint32_t iter = 0; iter < static_cast<uint32_t>(ceil((static_cast<double>(cd) - ab) / 2)); iter++) {
    tmp = cycle[ab + iter];
    cycle[ab + iter] = cycle[cd - iter];
    cycle[cd - iter] = tmp;
  }
}

void save_to_file(const std::string& filename, const std::array<std::array<int, 2>, N>& nodes, const std::vector<uint32_t>& cycle, double distance) {
  std::ofstream outFile(filename);
  if (!outFile) {
    std::cerr << "File cannot be loaded.\n";
    exit(1);
  } else {
    outFile << "x " << distance << std::endl;
    for (const uint32_t& node_id: cycle) {
      outFile << nodes[node_id][0] << " " << nodes[node_id][1] << std::endl;
    }
    outFile << nodes[cycle[0]][0] << " " << nodes[cycle[0]][1] << std::endl;
  }
  outFile.close();
}

std::vector<uint32_t> simulated_annealing(const std::string& T_type, const std::string& filename, const std::array<std::array<int, 2>, N>& V) {
  std::vector<uint32_t> P(N);
  std::vector<uint32_t> P_new(N);
  double d_P, d_P_new, r, T = 0.;
  uint32_t edge_ab = 0, edge_cd = 0;

  std::iota(P.begin(), P.end(), 0);
  std::random_shuffle(P.begin(), P.end());
  d_P = get_distance(V, P);
  save_to_file("before" + filename + ".dat", V, P, d_P);
  std::cout << "\n Initial distance   (" + filename + "): " << d_P << std::endl;
  
  
  for (uint32_t i = MIN_I; i >= 1; i--) {
    if (T_type == "linear") {
       T = T_MODIFIER * i;
    } else if (T_type == "square") {
      T = T_MODIFIER * pow(static_cast<double>(i), 2);
    } else {
      std::cout << "Wrong T type. selecting square variant." << std::endl;
      T = T_MODIFIER * pow(static_cast<double>(i), 2);
    }
    
    for (uint32_t it = 0; it < MAX_IT; it++) {
      edge_ab = 0, edge_cd = 0;
      while(abs((int)edge_ab - (int)edge_cd) <= 1 || (edge_ab == 0 && edge_cd == N - 1) || (edge_ab == N - 1 && edge_cd == 0)) {
        edge_ab = rand() % N;
        edge_cd = rand() % N;
      }

      P_new = P;

      swap_edges(edge_ab, edge_cd, P_new);

      d_P = get_distance(V, P);
      d_P_new = get_distance(V, P_new);
      if (d_P_new < d_P) {
        P = P_new;
      } else {
        r = ((double) rand() / (RAND_MAX));
        if (r < exp((d_P_new - d_P) / -T)) {
          P = P_new;
        }
      }
    }
  }

  save_to_file("after" + filename + ".dat", V, P, d_P);
  std::cout << "\n Optimized distance (" + filename + "): " << get_distance(V, P) << std::endl;
  return P;
}