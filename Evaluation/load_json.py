import json
import csv
import argparse
import glob
import matplotlib.pyplot as plt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-docker_name", default='nnunet', help="docker名称")
    args = parser.parse_args()
    print('we are counting', args.docker_name)
    json_dir = './data_all/{}'.format(args.docker_name)
    csv_path = './data_all/{}/infer_Efficiency.csv'.format(args.docker_name)
    jsonl = glob.glob(json_dir + '/*.json')
    alldata = []
    for item in jsonl:
        csv_l = []
        name = item.split('/')[-1].split('.')[0]
        csv_l.append(name)
        zitem = item
        with open(zitem)as f:
            js = json.load(f)
            csv_l.append(js['time'])
            mem = js['gpu_memory']
            x = [item * 0.5 for item in range(len(mem))]
            plt.cla()
            plt.xlabel("Time (s)", Fontname='Times New Roman', fontsize='large')
            plt.ylabel("GPU Memory (MB)", Fontname='Times New Roman', fontsize='large')
            plt.plot(x, mem, "b", ms=10, label="a")
            plt.savefig(zitem.replace('.json', '.jpg'))
            count_set = set(mem)
            count_list = []
            for citem in count_set:
                cts = mem.count(citem)
                if cts > 0.02 * len(mem):
                    count_list.append(citem)
            max_mem = max(count_list)
            csv_l.append(max_mem)
        alldata.append(csv_l)
    f = open(csv_path, 'w')
    writer = csv.writer(f)
    writer.writerow(['name',
                     'all_flod_time', 'all_flod_gpumemory',
                     ])
    for i in alldata:
        writer.writerow(i)
    f.close()