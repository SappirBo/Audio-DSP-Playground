import subprocess
import os

def build_and_install():
  """Builds the library and installs it."""

  # Navigate to the library directory
  os.chdir("audio_process_lib")

  # Build the library using Maturin
  subprocess.run(["maturin", "build"], check=True)

  # Navigate back to the parent directory
  os.chdir("..")

  # Install the built wheel
  subprocess.run(["pip", "install", "--force-reinstall", "audio_process_lib/target/wheels/audio_process_lib-0.1.0-cp310-cp310-manylinux_2_34_x86_64.whl"], check=True)

if __name__ == "__main__":
  build_and_install()