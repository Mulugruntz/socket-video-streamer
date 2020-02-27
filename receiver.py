import socket
from struct import unpack
import sys
import numpy

import cv2


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def read_from_socket(sock: socket.socket, n: int, *, buffer: int = 1024) -> bytes:
    bdata = bytearray()
    while len(bdata) < n:
        data = sock.recv(min(buffer, n - len(bdata)))
        if not data:
            raise ConnectionAbortedError
        bdata += data
    return bytes(bdata)


def main():
    print("Initializing...")
    out = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            try:
                while True:
                    data = conn.recv(20)
                    if not data:
                        break
                    fps = unpack(">f", data[0:4])[0]
                    width = unpack(">f", data[4:8])[0]
                    height = unpack(">f", data[8:12])[0]
                    size = unpack(">q", data[12:20])[0]

                    if out is None:
                        # Define the codec and create VideoWriter object
                        out = cv2.VideoWriter(
                            filename="output3.mp4",
                            fourcc=0x7634706D,
                            fps=fps,
                            frameSize=(int(width), int(height),),
                            isColor=True,
                        )
                    try:
                        data = read_from_socket(conn, size)
                    except ConnectionAbortedError:
                        break
                    finally:
                        frame = numpy.ndarray(
                            (int(width), int(height), 3), dtype="uint8", buffer=data
                        )
                        out.write(frame)

            except Exception as e:
                print("ERROR!", sys.exc_info())
            finally:
                out.release()
                cv2.destroyAllWindows()
    print("Done!")


if __name__ == "__main__":
    main()
