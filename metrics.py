def print_metrics(sender, receiver):
    sent = sender.sent_packets
    received = receiver.received_packets

    loss = 1 - (received / sent) if sent > 0 else 0

    print("\n=== METRICS ===")
    print(f"Sent: {sent}")
    print(f"Received: {received}")
    print(f"Loss Rate: {loss:.2f}")
