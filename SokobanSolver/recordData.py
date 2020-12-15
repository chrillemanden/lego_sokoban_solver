import os

maps = ["testmapCompareBFSvsA.txt", "testmapCompareBFSvsA2.txt","testmap1.txt","testmap2.txt","testmap3.txt"]
for algo in range(2):
	for map in maps:
		for current_test in range(5):			
			print(map +" "+ str(algo)+" "+ str(current_test))
			os.system("python3 main.py " + map + " " + str(algo)+" " +str(current_test))
