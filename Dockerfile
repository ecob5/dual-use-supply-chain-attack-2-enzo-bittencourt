# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git and other essential tools for development
RUN apt-get update && apt-get install -y \
    git \
    vim \
    nano \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/magikboy/Currency-Exchange.git .

# Install Python development tools
RUN pip install --upgrade pip && \
    pip install \
    black \
    flake8 \
    pytest \
    ipython \
    jupyter

# Create a non-root user for development
RUN useradd -m -s /bin/bash developer && \
    chown -R developer:developer /app

# Switch to non-root user
USER developer

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port for Jupyter (optional)
EXPOSE 8888

# Default command - start bash shell for development
CMD ["/bin/bash"]
