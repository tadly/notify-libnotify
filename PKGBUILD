pkgname=notify-libnotify
pkgver=0.0.3
pkgrel=1
pkgdesc="libnotify client to be used with the android app."
arch=('any')
license=('GPLv3')
depends=(
    'python'
    'python-lwe-mapper'
    'python-lwe-mjs'
)
source=("git+https://github.com/Tadly/notify-libnotify")
md5sums=('SKIP')

package() {
    cd ${pkgname}
    python3 setup.py install --root=$pkgdir/ --optimize=1
}
