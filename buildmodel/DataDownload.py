from os import makedirs, path, rename, rmdir
from tarfile import open as open_tar
from urllib import request, parse


# This program downloads all the data from
# the apache spam assassin website
def download_corpus(dataset_dir: str = 'data'):
    # Where the website is located
    base_url = 'https://spamassassin.apache.org'
    # directory on the website for the data
    corpus_path = 'old/publiccorpus'
    # files to download
    files = {
        '20030228_easy_ham.tar.bz2': 'ham',
        '20030228_spam.tar.bz2': 'spam',
    }

    # ------ Create Directories ------ #

    # downloads will store all the actual data
    # ham will store non spam emails
    # spam will store all the spam emails
    downloads_dir = path.join(dataset_dir, 'downloads')
    ham_dir = path.join(dataset_dir, 'ham')
    spam_dir = path.join(dataset_dir, 'spam')

    makedirs(downloads_dir, exist_ok=True)
    makedirs(ham_dir, exist_ok=True)
    makedirs(spam_dir, exist_ok=True)

    # ------------------------------- #

    for file, spam_or_ham in files.items():
        # download file
        url = parse.urljoin(base_url, f'{corpus_path}/{file}')
        tar_filename = path.join(downloads_dir, file)
        request.urlretrieve(url, tar_filename)

        # list e-mails in compressed file
        emails = []
        with open_tar(tar_filename) as tar:
            tar.extractall(path=downloads_dir)
            for tarinfo in tar:
                if len(tarinfo.name.split('/')) > 1:
                    emails.append(tarinfo.name)

        # move e-mails to ham or spam dir
        for email in emails:
            directory, filename = email.split('/')
            directory = path.join(downloads_dir, directory)
            rename(path.join(directory, filename),
                   path.join(dataset_dir, spam_or_ham, filename))

        rmdir(directory)