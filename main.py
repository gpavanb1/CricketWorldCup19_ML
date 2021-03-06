from tabulate import tabulate
import helper


# Number of samples for Monte Carlo
num_samples = 30000
table = helper.gen_pool_stage_prob(num_samples)

# Display output
print(tabulate(table, headers='keys', tablefmt='psql', showindex=False))

