import cv2
from Enc_Dec import EncryptionManager
import numpy as np


class ImageSteganography:
    @staticmethod
    def embed_message(image, message):
        key, nonce, cipher_text = EncryptionManager.encrypt_message(message)
        print(f"Encrypted message: {cipher_text}")

        # Convert image to YCrCb color space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        Y, Cr, Cb = cv2.split(image)

        # Convert cipher_text to binary
        message_bits = ''.join(format(byte, '08b') for byte in cipher_text)
        message_length = len(message_bits)  # Length of the message in bits

        # Add message length as metadata (32 bits)
        length_bits = format(message_length, '032b')
        message_bits = length_bits + message_bits + '00000000'  # Null terminator

        # Check if the message fits into the image
        if len(message_bits) > Y.size:
            raise ValueError("Message is too large to embed in the given image.")

        index = 0

        # Embed the message in the LSB of Y Channel
        for i in range(Y.shape[0]):
            for j in range(Y.shape[1]):
                if index < len(message_bits):
                    # Clear the LSB and set it to the message bit
                    Y[i, j] = np.uint8(Y[i, j] & 0b11111110) | int(message_bits[index])
                    index += 1

        # Merge channels and convert back to BGR
        image = cv2.merge((Y, Cr, Cb))
        image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

        return image, key, nonce

    @staticmethod
    def extract_message(image, key, nonce):
        # Convert image to YCrCb color space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        Y, _, _ = cv2.split(image)

        message_bits = ''

        # Extract message from LSB of Y channel
        for i in range(Y.shape[0]):
            for j in range(Y.shape[1]):
                lsb = Y[i, j] & 1
                message_bits += str(lsb)

        # Extract the length of the message (first 32 bits)
        message_length = int(message_bits[:32], 2)
        message_bits = message_bits[32:]

        # Extract the cipher text bits
        cipher_text = bytearray()
        for i in range(0, len(message_bits), 8):
            byte = message_bits[i:i + 8]
            if len(byte) < 8:  # Skip incomplete chunks at the end
                break
            if byte == "00000000":  # Null terminator
                break
            try:
                cipher_text.append(int(byte, 2))
            except ValueError as e:
                print(f"Invalid byte during conversion: {byte}")
                raise e
        print(f"Extracted cipher text: {cipher_text}")

        # Decrypt the message
        plain_text = EncryptionManager.decrypt_message(key, nonce, bytes(cipher_text))
        print(f"Decrypted message: {plain_text}")
        return plain_text
