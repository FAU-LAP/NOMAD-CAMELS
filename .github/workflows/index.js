const core = require('@actions/core');
const exec = require('@actions/exec');


// most @actions toolkit packages have async methods
async function run() {
  try {
    // Qt installer assumes basic requirements that are not installed by
    // default on Ubuntu.
    if (process.platform === 'linux') {
      await exec.exec('sudo apt-get update')
      await exec.exec(
        'sudo apt-get install -y libegl1 libdbus-1-3 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xinput0 libxcb-xfixes0 x11-utils libxcb-cursor0'
      )
    }
  } catch (error) {
    core.setFailed(error.message)
  }
}

run();