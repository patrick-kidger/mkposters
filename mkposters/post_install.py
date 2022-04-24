import subprocess


def main():
    bash_cmd = """
    # Detect the compute architecture (linux-arm64, macos-arm64, macos-x64) and download the appropriate distribution release of dart-sass
    # https://github.com/sass/dart-sass/releases/tag/1.50.1

    sass_release="1.50.1"
    arch=$(uname -m)
    kernel=$(uname -s)

    echo Detected architecture: $arch and kernel: $kernel.

    if [[ "$arch" =~ ^(arm64|aarch64)$ ]] && [ "$kernel" = "Linux" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/${sass_release}/dart-sass-${sass_release}-linux-arm64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
    elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Linux" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/${sass_release}/dart-sass-${sass_release}-linux-x64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
    elif [ "$arch" = "arm64" ] && [ "$kernel" = "Darwin" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/${sass_release}/dart-sass-${sass_release}-macos-arm64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
    elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Darwin" ]; then
        curl -sL "https://github.com/sass/dart-sass/releases/download/${sass_release}/dart-sass-${sass_release}-macos-x64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
    else
        echo "Unsupported architecture: $arch and kernel: $kernel"
    fi

    # move the dart-sass binary to the correct location
    mkloc=$(pip show mkposters | grep Location | cut -d ' ' -f 2)
    rm -rf $mkloc/mkposters/third_party/dart-sass && mv dart-sass $mkloc/mkposters/third_party
    echo "Downloaded from https://github.com/sass/dart-sass/releases/download/${sass_release} \nSee also:\nhttps://sass-lang.com/install\ninstalled version: ${sass_release}" > "${mkloc}/mkposters/third_party/dart-sass/SASSBUILT.txt"
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
    main()
