from email import message_from_file
from glob import glob
import numpy as np


def get_emails_and_labels(ham_dir, spam_dir):
    """
    :param ham_dir: location of the ham directory relative to project folder
    :param spam_dir: location of the spam directory relative to project folder
    :return emails: a numpy array of M cells (M: No. of emails) each being of type
                    EmailFormat.SimplifiedEmail
    :return labels: whether each respective email is spam (1) or not-spam (0)
    """

    ham_email_iterator = EmailIterator(ham_dir)
    spam_email_iterator = EmailIterator(spam_dir)
    ham_emails = np.array([email for email in ham_email_iterator])
    spam_emails = np.array([email for email in spam_email_iterator])
    emails = np.concatenate((ham_emails, spam_emails))
    labels = np.concatenate((np.zeros(ham_emails.size), np.ones(spam_emails.size)))
    return emails, labels


class SimplifiedEmail:
    """
    Eliminates the messy original format of a MIME email
    Included content entails To, From, Cc, Subject, Body(payload)
    """

    def __init__(self, email, is_dict=False):
        if is_dict:
            self.destination = email['to']
            self.source = email['from']
            self.copies = email['cc']
            self.subject = email['subject']
            self.payload = [email['body']]
        else:
            self.payload = []
            self._unbox_payload(email)

            self.destination = email.get('To')
            self.source = email.get('From')
            self.copies = email.get('Cc')
            self.subject = email.get('Subject')

    def unify_payload(self, join_character=' ') -> str:
        """
        Brings a complex tree of payloads into a single linear string

        :param join_character: character to combine each payload with
        :return: Unified Payload as a string
        """
        return join_character.join(self.payload)

    # returns all the data besides the body(payload)
    # you can choose to get a dictionary instead of
    # an array using the isDictionary parameter
    def get_headers(self, is_dict=False):
        """
        returns header information about the email

        :param is_dict: if true returns a dictionary form instead of array
        :return: header information
        """

        if is_dict:
            headers = {
                'To': self.destination,
                'From': self.source,
                'Cc': self.copies,
                'Subject': self.subject,
            }
            return headers

        headers = [('To', self.destination), ('From', self.source), ('Cc', self.copies), ('Subject', self.subject)]
        return headers

    def _unbox_payload(self, message) -> None:
        """
        Recursively breaks down complex payloads into a single linear array

        :param message: Email.message.message
        """
        if message.is_multipart():
            # if a message is multipart then it returns an array
            # that consists either of Strings or another
            # email.message.Message object
            for subMessage in message.get_payload():
                if type(subMessage) == str:
                    self.payload.append(subMessage)
                else:
                    self._unbox_payload(subMessage)
        else:
            self.payload.append(message.get_payload())

    def __str__(self):
        s = ''
        # header information
        headers = self.get_headers()
        for header in headers:
            s += str(header[0]) + ': ' + str(header[1]) + '\n'
        # payload information
        s += 'Payload: \n' + self.unify_payload()

        return s

    def __repr__(self):
        return self.__str__()


class EmailIterator:
    """
    A method for going through each individual email in
    MIME format and converting it into a EmailFormat.SimplifiedEmail
    """

    def __init__(self, directory):
        self._files = glob(f'{directory}/*')
        self._pos = 0

    def __iter__(self):
        self._pos = -1
        return self

    def __next__(self):
        if self._pos < len(self._files) - 1:
            self._pos += 1
            return self.parse_email(self._files[self._pos])
        raise StopIteration()

    # converts a raw email into a simplified email
    @staticmethod
    def parse_email(filename: str) -> SimplifiedEmail:
        """
        Converts a raw MIME email into a SimplifiedEmail

        :param filename: path to MIME email
        :return: EmailFormat.SimplifiedEmail Instance
        """
        with open(filename,
                  encoding='utf-8',
                  errors='replace') as fp:
            email = message_from_file(fp)
            return SimplifiedEmail(email)
