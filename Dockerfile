FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy the Wake-on-LAN sender script
COPY wol_sender.py /app/

# Make the script executable
RUN chmod +x /app/wol_sender.py

# Create a non-root user for security
RUN addgroup -g 1000 wol && \
    adduser -D -s /bin/sh -u 1000 -G wol wol

# Change ownership of the app directory
RUN chown -R wol:wol /app

# Switch to non-root user
USER wol

# Set the default command
CMD ["python3", "/app/wol_sender.py"]

# Add labels for documentation
LABEL maintainer="DockerNudge" \
      description="Docker container to send Wake-on-LAN packets" \
      version="1.0"