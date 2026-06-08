# Mocking — mock the edge, use the real thing in the middle

A mock encodes *your assumption* about how a dependency behaves. If the assumption is
wrong, the test stays green while production breaks. So mock as little as possible.

## When to mock

- **Genuinely external, slow, or non-deterministic boundaries**: third-party HTTP APIs,
  paid services, the system clock, randomness, the network to a remote host you don't
  control.
- **To force an error path** that's hard to trigger for real (a connection reset, a
  timeout, a malformed response).

## When NOT to mock

- **Your own code** under test — test it for real.
- **Protocol / wire logic** — do not mock the socket and assert you called `send()` with
  bytes *you* computed; that just tests your test. Stand up a **real loopback socket** and
  assert the round-trip. The OS TCP/UDP stack on `127.0.0.1` is fast and deterministic.
- **Pure functions** — no I/O, nothing to mock.

## Network-protocol integration example (pytest)

Prefer a real loopback round-trip over a mocked socket — it catches framing, encoding, and
ordering bugs a mock would hide:

```python
import socket, threading

def echo_once(sock):
    conn, _ = sock.accept()
    with conn:
        conn.sendall(conn.recv(1024))

def test_frame_roundtrips_over_a_real_socket():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))            # port 0 = let the OS pick a free port
    srv.listen(1)
    threading.Thread(target=echo_once, args=(srv,), daemon=True).start()

    cli = socket.create_connection(srv.getsockname(), timeout=2)
    frame = encode_frame(kind="DATA", payload=b"hi")     # the code under test
    cli.sendall(frame)
    got = cli.recv(1024)
    assert decode_frame(got).payload == b"hi"            # real bytes, real round-trip
```

Mock only the parts you can't run locally (e.g. a remote STUN server) — and even then,
prefer a tiny real local stand-in over a `Mock()` when feasible.

## Rule of thumb

The more a mock has to *know* about the thing it replaces, the more likely the test is
testing the mock. Push mocks to the true edges; keep the middle real.
