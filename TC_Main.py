import TC_Class

list_crane, list_trailer, list_unit, list_grid, index_crane, index_trailer, index_unit = TC_Class.read_location('location.xlsx')
GA1 = TC_Class.GeneticAlgorithm(list_crane, list_trailer, list_unit, list_grid, index_crane, index_trailer, index_unit)
GA1.parameters(number_generation=100, size_population=100, rate_crossover=0.5, rate_mutation=0.1)

print(GA1.GA())
