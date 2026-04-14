# ---------- Stage 1: rustpiler build ----------
FROM lukemathwalker/cargo-chef:latest-rust-slim-bookworm AS chef
WORKDIR /build

RUN apt-get update && apt-get install -y musl-tools \
  && rm -rf /var/lib/apt/lists/*

RUN rustup target add x86_64-unknown-linux-musl

FROM chef AS planner
COPY rustpiler/ ./rustpiler
WORKDIR /build/rustpiler
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
WORKDIR /build/rustpiler

COPY --from=planner /build/rustpiler/recipe.json recipe.json

# build statically linked bin for nsjail
RUN cargo chef cook --release --target x86_64-unknown-linux-musl --recipe-path recipe.json

COPY rustpiler/ .

RUN cargo build --release --target x86_64-unknown-linux-musl
RUN strip target/x86_64-unknown-linux-musl/release/rustpiler

# ---------- Stage 2: nsjail build ----------
FROM debian:bookworm AS nsjail-builder

RUN apt-get update && apt-get install -y \
  git \
  build-essential \
  flex \
  bison \
  pkg-config \
  libprotobuf-dev \
  protobuf-compiler \
  libnl-3-dev \
  libnl-route-3-dev \
  libcap-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# install and pin nsjail 3.5
RUN git clone https://github.com/google/nsjail.git \
  && cd nsjail \
  && git checkout 402e2b4 
WORKDIR /build/nsjail

RUN make

# ---------- Stage 3: runtime ----------
FROM python:3.14-slim

WORKDIR /app

# minimal runtime deps
RUN apt-get update && apt-get install -y \
  util-linux \
  libnl-3-200 \
  libnl-route-3-200 \
  libprotobuf32 \
  libcap2 \
  && rm -rf /var/lib/apt/lists/*

# copy rustpiler
COPY --from=builder /build/rustpiler/target/release/rustpiler /usr/local/bin/rustpiler

# copy nsjail binary
COPY --from=nsjail-builder /build/nsjail/nsjail /usr/local/bin/nsjail

# python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
