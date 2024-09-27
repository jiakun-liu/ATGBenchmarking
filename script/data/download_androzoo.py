import argparse
import os

import pandas as pd
import concurrent.futures

APIKEY = "*****************"

def exclude_processed(df_sampled, df_processed):
    df_sampled = df_sampled[~df_sampled['sha256'].isin(df_processed['sha256'])]
    return df_sampled


def downloading(sha256, file_path):
    if os.path.exists(f"{sha256}.apk"):
        os.remove(f"{sha256}.apk")
    cmd = f"curl -O --remote-header-name -G -d apikey={APIKEY} -d sha256={sha256} https://androzoo.uni.lu/api/download"
    print(cmd)
    os.system(cmd)
    if os.path.exists(f"{sha256}.apk"):
        os.rename(f"{sha256}.apk", file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process to download fdroid.')

    # Define the arguments
    parser.add_argument('--apks_to_download', type=str, help='Path to the file containing apks to download')
    parser.add_argument('--apk_dir', type=str, help='Directory to save downloaded APKs')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    apks_to_download = args.apks_to_download
    apk_dir = args.apk_dir

    print(f'APKs Path: {apks_to_download}')
    print(f'APK Directory: {apk_dir}')

    if not os.path.exists(apk_dir):
        os.makedirs(apk_dir)

    apks_to_download_df = pd.read_csv(apks_to_download)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=30)

    for index, row in apks_to_download_df.iterrows():
        apkname = row['pkg_name']
        version = row['vercode']
        sha256 = row['sha256']
        print(apkname, version, sha256)
        file_path = f"{apk_dir}/{apkname}_{version}.apk"
        if os.path.exists(file_path):
            print(f"File {file_path} already exists")
            continue
        executor.submit(downloading, sha256, file_path)

