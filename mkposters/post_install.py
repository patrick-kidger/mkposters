import pathlib
import subprocess


def post_install(package_dir: str, sass_release: str = "1.50.1"):
    """
    Run post-install of dart-sass.
    Detect the compute architecture (linux-arm64, linux-x64, macos-arm64, macos-x64) and download the appropriate distribution release of dart-sass.
    See also: https://github.com/sass/dart-sass/releases

    Args:
        package_dir (str): The location of `mkposters`. This is the directory that contains the `third_party` folder which dart-sass should be installed in.
        sass_release (str): The release version of sass to download.
    Returns:
        None

    """  # noqa: E501

    sass_dir = pathlib.Path(package_dir) / "third_party"

    bash_cmd = f"""
    # Detect the compute architecture (linux-arm64, macos-arm64, macos-x64) and download the appropriate distribution release of dart-sass
    # https://github.com/sass/dart-sass/releases/tag/1.50.1

    arch=$(uname -m)
    kernel=$(uname -s)

    echo Detected architecture: $arch and kernel: $kernel.

    if [[ "$arch" =~ ^(arm64|aarch64)$ ]] && [ "$kernel" = "Linux" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-linux-arm64.tar.gz" > {sass_dir}/dart.tar.gz && tar -xzf {sass_dir}/dart.tar.gz --directory {sass_dir} && rm {sass_dir}/dart.tar.gz && chmod 755 {sass_dir}/dart-sass/sass
        echo "Downloaded https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-linux-arm64.tar.gz \nSee also:\nhttps://sass-lang.com/install\ninstalled version: {sass_release}" > "{sass_dir}/dart-sass/SASSBUILT.txt"

    elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Linux" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-linux-x64.tar.gz" > {sass_dir}/dart.tar.gz && tar -xzf {sass_dir}/dart.tar.gz --directory {sass_dir} && rm {sass_dir}/dart.tar.gz && chmod 755 {sass_dir}/dart-sass/sass
        echo "Downloaded https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-linux-x64.tar.gz \nSee also:\nhttps://sass-lang.com/install\ninstalled version: {sass_release}" > "{sass_dir}/dart-sass/SASSBUILT.txt"

    elif [ "$arch" = "arm64" ] && [ "$kernel" = "Darwin" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-macos-arm64.tar.gz" > {sass_dir}/dart.tar.gz && tar -xzf {sass_dir}/dart.tar.gz --directory {sass_dir} && rm {sass_dir}/dart.tar.gz && chmod 755 {sass_dir}/dart-sass/sass
        echo "Downloaded https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-macos-arm64.tar.gz \nSee also:\nhttps://sass-lang.com/install\ninstalled version: {sass_release}" > "{sass_dir}/dart-sass/SASSBUILT.txt"

    elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Darwin" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-macos-x64.tar.gz" > {sass_dir}/dart.tar.gz && tar -xzf {sass_dir}/dart.tar.gz --directory {sass_dir} && rm {sass_dir}/dart.tar.gz && chmod 755 {sass_dir}/dart-sass/sass
        echo "Downloaded https://github.com/sass/dart-sass/releases/download/{sass_release}/dart-sass-{sass_release}-macos-x64.tar.gz \nSee also:\nhttps://sass-lang.com/install\ninstalled version: {sass_release}" > "{sass_dir}/dart-sass/SASSBUILT.txt"

    else
        echo "Unsupported architecture: $arch and kernel: $kernel"
    fi

    """  # noqa: E501

    with subprocess.Popen(
        bash_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
        close_fds=True,
        shell=True,
        executable="/bin/bash",
    ) as proc:
        if proc.stdout:
            with proc.stdout:
                for line in iter(proc.stdout.readline, b""):
                    print(line.decode().rstrip())

        exit_code = proc.wait()
        if exit_code != 0:
            raise Exception(f"post_install.py failed with exit code {exit_code}")


if __name__ == "__main__":
    post_install()
