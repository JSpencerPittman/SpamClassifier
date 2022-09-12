from email import message_from_file
from glob import glob
import numpy as np


def getEmailsAndLabels(ham_dir, spam_dir):
    hamEmailIterator = EmailIterator(ham_dir)
    spamEmailIterator = EmailIterator(spam_dir)
    hamEmails = np.array([email for email in hamEmailIterator])
    spamEmails = np.array([email for email in spamEmailIterator])
    emails = np.concatenate((hamEmails, spamEmails))
    labels = np.concatenate((np.zeros(hamEmails.size), np.ones(spamEmails.size)))
    return emails, labels


# Eliminates the messy original format of a MIME email
# Included content entails To, From, Cc, Subject, Body(payload)
class SimplifiedEmail:

    def __init__(self, email, isDict=False):
        if isDict:
            self.destination = email['to']
            self.source = email['from']
            self.copies = email['cc']
            self.subject = email['subject']
            self.payload = [email['body']]
        else:
            self.payload = []
            self._unboxPayload(email)

            self.destination = email.get('To')
            self.source = email.get('From')
            self.copies = email.get('Cc')
            self.subject = email.get('Subject')


    # Many emails have multiple payloads so this function
    # combines them into a single string
    def unifyPayload(self, joinCharacter=' '):
        return joinCharacter.join(self.payload)

    # returns all the data besides the body(payload)
    # you can choose to get a dictionary instead of
    # an array using the isDictionary parameter
    def getHeaders(self, isDictionary=False):
        if isDictionary:
            headers = {
                'To': self.destination,
                'From': self.source,
                'Cc': self.copies,
                'Subject': self.subject,
            }
            return headers

        headers = []
        headers.append(('To', self.destination))
        headers.append(('From', self.source))
        headers.append(('Cc', self.copies))
        headers.append(('Subject', self.subject))
        return headers

    # recursivley breaks down complex payloads into a single
    # linear array
    def _unboxPayload(self, message):
        if message.is_multipart():
            # if a message is multipart then it returns an array
            # that consists either of Strings or another
            # email.message.Message object
            for subMessage in message.get_payload():
                if type(subMessage) == str:
                    self.payload.append(subMessage)
                else:
                    self._unboxPayload(subMessage)
        else:
            self.payload.append(message.get_payload())

    def __str__(self):
        s = ''
        # header information
        headers = self.getHeaders()
        for header in headers:
            s += str(header[0]) + ': ' + str(header[1]) + '\n'
        # payload information
        s += 'Payload: \n' + self.unifyPayload()

        return s

    def __repr__(self):
        return self.__str__()

    # A method for going through each individual


# email and converting it into a SimpleEmail
class EmailIterator:
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
        with open(filename,
                  encoding='utf-8',
                  errors='replace') as fp:
            email = message_from_file(fp)
            return SimplifiedEmail(email)

