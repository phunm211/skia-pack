#! /usr/bin/env python3

import common, os, shutil, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))

  build_type = common.build_type()
  machine = common.machine()
  host = common.host()
  host_machine = common.host_machine()
  target = common.target()
  ndk = common.ndk()

  tools_dir = "depot_tools"
  ninja = 'ninja.bat' if 'windows' == host else 'ninja'
  isIos = 'ios' == target or 'iosSim' == target
  isTvos = 'tvos' == target or 'tvosSim' == target
  isIosSim = 'iosSim' == target
  isTvosSim = 'tvosSim' == target
  isMacos = 'macos' == target

  if build_type == 'Debug':
    args = ['is_debug=true']
  else:
    args = ['is_official_build=false']

  args += [
    'target_cpu="' + machine + '"',
    'skia_use_system_expat=false',
    'skia_use_system_libjpeg_turbo=false',
    'skia_use_system_libpng=false',
    'skia_use_system_libwebp=false',
    'skia_use_system_zlib=false',
    'skia_use_sfntly=false',
    'skia_use_system_freetype2=false',
    'skia_use_system_icu=false'
  ]

  if 'android' == target:
    args += [
      'ndk="'+ ndk + '"',
      'skia_use_gl=true',
      'skia_use_egl=true',
      'skia_enable_gpu=true',
      'skia_use_freetype=true',
      'is_trivial_abi=false',
      'use_cfi=true',
      'use_rtti=true',
      'use_lto=true',
      'skia_use_harfbuzz=true',
      'is_official_build=false'
    ]

  if 'linux' == host and 'arm64' == host_machine:
    tools_dir = 'tools'
    ninja = 'ninja-linux-arm64'

  out = os.path.join('out', build_type + '-' + target + '-' + machine)
  gn = 'gn.exe' if 'windows' == host else 'gn'
  print([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  subprocess.check_call([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  subprocess.check_call([os.path.join('..', tools_dir, ninja), '-C', out, 'skia', 'modules'])

  return 0

if __name__ == '__main__':
  sys.exit(main())
