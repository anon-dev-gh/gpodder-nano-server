# Three targets
#    builder to build the requirements
#    prod is the source itself
#    devcontainer is built on top of prod and adds tooling for the devcontainer

FROM python:3.10-slim as builder
# pip will install at /home/$USERNAME/local/.bin that is not part of PATH
# TODO: Can this path modification be done at useradd time?
# ENV PATH="$PATH:/home/$USERNAME/.local/bin/"

# Build the requirements files using pipenv and Pipfile
COPY Pipfile ./

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv lock \
    && pipenv requirements > /tmp/requirements.txt \
    && pipenv requirements --dev-only > /tmp/requirements-dev.txt

FROM python:3.10-slim as prod
# Copy the requirements and install them

COPY --from=builder /tmp/requirements.txt /tmp/
RUN pip --no-cache-dir install --upgrade pip \
    && pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt

FROM prod as devcontainer
# Additionally install dev-requirements and tools
COPY --from=builder /tmp/requirements-dev.txt /tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-dev.txt

# Adds a vscode non-root user following
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh
# Install tig  (git interface)
#         curl (download starship)
#         zsh  (shell for the container)
RUN apt-get update && apt-get install -y tig curl zsh

# Set to the new user
USER $USERNAME

# Install starship
# Note we are using ~ folders to avoid sudoing.
RUN mkdir -p ~/.local/bin \
    # download starship
    && (curl -fsSL https://starship.rs/install.sh | sh -s -- -y -b ~/.local/bin/) \
    # configure starship
    # Couldn't make ENV work to add $HOME/.local/bin
    # Coudln't make HERE doc work to write $HOME/.zshrc
    # Thus, good-old echo and append to file
    && echo 'export PATH=$PATH:$HOME/.local/bin/' >> $HOME/.zshrc \
    && echo 'eval "$(starship init zsh)"' >> $HOME/.zshrc \
    && mkdir -p ~/.config/ \
    # At this point PATH is not expanded to include ~/.local/bin/ so we need to hardcode it
    && ~/.local/bin/starship preset plain-text-symbols -o ~/.config/starship.toml
