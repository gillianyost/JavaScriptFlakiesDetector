# argument 1: Results folder stress
# argument 2: Results folder no stress
# argument 3: Number of runs
# argument 4: Time data stress
# argument 5: Time data no stress

python3 manualFlakieFinder.py $1 $3
python3 manualFlakieFinder.py $2 $3
python3 flakie_parser.py $1 $3 server_complete_s.json $4 clean
python3 flakie_parser.py $2 $3 server_complete_ns_5.json $5 clean
python3 ./data_parser.py ./server_data_complete_s.json ./data_agg_s.csv
python3 ./data_parser.py ./server_data_complete_ns.json ./data_agg_ns.csv
python3 ./run_comp.py data_agg_s.csv data_agg_ns.csv completeCommonFlakies.txt stressOnly.txt noStressOnly.txt

# python3 flakie_parser_single.py ./server_data_complete_ns.json $2 data_agg_s.csv data_agg_ns.csv server_data_only_ns.json