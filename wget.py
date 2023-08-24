from urllib.request import urlretrieve

from tqdm import tqdm

class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize

def download(eg_link, filename):
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                desc=eg_link.split('/')[-1]) as t:  # all optional kwargs
        urlretrieve(eg_link, filename=filename,
                        reporthook=t.update_to)
        t.total = t.n