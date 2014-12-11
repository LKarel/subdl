# Maintainer: Ragnis Armus <ragnis.armus@gmail.com>
pkgname=subdl-git
pkgver=0.0.0
pkgrel=1
pkgdesc='Intelligent subtitle downloader'
arch=('i686' 'x86_64')
license=('MIT')
depends=('python3' 'python-beautifulsoup4')
makedepends=('git')
provides=('subdl')
_gitroot='https://github.com/Ragnis/subdl.git'
_gitname=subdl

build ()
{
	if [[ -d "$srcdir/$_gitname" ]]; then
		rm -rf "$srcdir/$_gitname"
	fi

	git clone "$_gitroot"
}

package() {
	install -d "$pkgdir/usr/share"
	install -d "$pkgdir/bin"

	cp -r "$srcdir/$_gitname" "$pkgdir/usr/share/$pkgname"
	ln -s "/usr/share/$pkgname/main.py" "$pkgdir/bin/subdl"

	chmod a+x "$pkgdir/usr/share/$pkgname/main.py"
}
