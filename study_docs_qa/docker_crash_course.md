# Docker Crash Course — Q&A

---

## Part 1 — Why containers exist

### Development setup

**Q: What is Docker?**
A: **Docker** packages an application with its libraries, runtime, and environment configuration into one unit you can share and run. That unit runs as a **container**: an isolated environment that starts from a pre-built package, so the same command works on every operating system and for every service.

**Q: What goes wrong when every developer installs services on the host?**
A: Each person installs and configures Postgres, Redis, a message broker, and the rest directly on their OS. The steps differ between macOS, Windows, and Linux, a long install-and-configure sequence fails often, and ten services means ten installs. Two versions of the same service usually cannot share one OS install.

**Q: How does a container replace that install?**
A: The service and a specific version live inside the image. One Docker command downloads that package and starts it. The command does not change with the host OS or with which service you need, and two versions of the same service can run side by side because each has its own filesystem.

### Deployment

**Q: How did a deploy work before containers?**
A: Developers handed operations an artifact, such as a JAR, plus a written guide for installing the app and its database on the server OS. Missing steps in that guide caused back-and-forth, and two services that needed different versions of the same library conflicted on the host.

**Q: What does operations do once the app is an image?**
A: They run one command to start the application image and one command per dependency image. Configuration that used to live in the guide is already inside the image. Installing the Docker runtime on the server is a one-time step; after that, any image can run there.

---

## Part 2 — Kernel vs virtual machines

### What is virtualized

**Q: What are the two layers of an operating system?**
A: The **kernel** talks to hardware and hands out CPU, memory, and storage. The **applications layer** is everything you run on top of that kernel.

**Q: What does a container virtualize, and what does a virtual machine virtualize?**
A: A container ships the applications layer and uses a Linux **kernel** it did not boot itself. On a Linux engine that kernel is the host's. A **virtual machine** ships the applications layer and its own kernel, so it is a full guest OS. Docker images are usually megabytes and start in milliseconds. VM images are often gigabytes and take minutes, because every start boots a kernel.

**Q: Why can a Linux image fail on a Windows or Mac host?**
A: A Linux applications layer needs a Linux kernel. A Windows kernel cannot run it directly. A VM image does not have this limit: any guest OS can boot on any host, because the guest brings its own kernel. Docker was built for Linux first.

**Q: How does Docker Desktop run Linux images on Windows and macOS?**
A: **Docker Desktop** puts a small Linux distribution on a hypervisor, and containers use that Linux kernel. On current Windows, that Linux is a WSL2 distro. On Linux, the engine package (`docker-ce`) uses the host kernel directly. Docker Desktop for Linux still runs a VM. Install the engine when you only need the CLI.

---

## Part 3 — Clients

### Engine, CLI, and UI

**Q: What do you install?**
A: Follow the current official install page. Steps and system requirements change, and a Mac install is a different package for Intel and Apple silicon. **Docker Desktop** includes the **engine** (the service that runs containers), a **CLI**, and a **GUI**. On Linux you can install the engine and CLI without Desktop.

**Q: How do you know the engine is ready?**
A: Start Docker Desktop and wait until it reports the engine is running. Then `docker version` prints a client section and a server section. Commands fail with a daemon error when the engine is stopped. `docker images` lists local images and `docker ps` lists running containers. Both are empty on a fresh install.

**Q: When do you use the GUI instead of the CLI?**
A: The Desktop UI lists images and containers, running and stopped, and can start, stop, restart, delete, and create a container. It drives the same engine as the CLI. Use whichever you can operate without guessing. The commands in this file are the ones you need in a terminal and in CI.

---

## Part 4 — Images, registries, and tags

### Image vs container

**Q: What is an image?**
A: An **image** is the package, like a JAR or tarball, plus the OS applications layer, the runtime (Node and npm, a JRE, Python), files, directories, and environment variables the process needs. It is a read-only blueprint. Building or pulling creates it. It does not run by itself.

**Q: What is a container?**
A: A **container** is a running instance of an image. Starting the image launches its process inside the pre-configured filesystem. One image can start many containers, which is how you run several copies for capacity. Stopping a container does not delete the image.

**Q: Are image and container interchangeable in commands?**
A: No. `docker pull`, `docker build`, `docker images`, and `docker rmi` take an image. `docker run` creates a container from an image. `docker ps`, `docker logs`, `docker stop`, `docker start`, and `docker rm` take a container id or name.

### Registries and official images

**Q: Where do images come from?**
A: A **registry** is storage for images. **Docker Hub** is the largest public registry and the default the client searches, so `nginx` means Docker Hub unless you name another host. You can browse Hub without an account. Companies also publish to private registries.

**Q: What is a Docker official image?**
A: An image with the **Docker official image** badge. A Docker team reviews and publishes it together with the software's maintainers and with security review, so production defaults (user, ports, entrypoint, tags) are considered. Prefer it over a random image that wraps the same software.

**Q: How do a registry, a repository, and a tag differ?**
A: The **registry** is the service (Docker Hub, AWS ECR, Google Artifact Registry, Azure Container Registry, Nexus). A **repository** is one application inside that registry. A **tag** is one version inside the repository. `nginx:1.23` is repository `nginx`, tag `1.23`, on the default registry. A private name looks like `123456789.dkr.ecr.eu-west-1.amazonaws.com/node-app:1.0`.

**Q: When do you use a private registry?**
A: When the image is your application and must not be world-readable. Hub can host private repositories. Cloud registries (ECR and the others) are the usual company choice because CI can push there and servers can pull from there.

### Tags

**Q: What happens if you omit the tag?**
A: Docker uses the tag `latest`. Publishers usually move `latest` to the newest build, but it is only a label, not a version calculation. A later pull can silently change what `latest` means.

**Q: Which tag should you run?**
A: A specific version, such as `nginx:1.27` or `postgres:16`. Pinning is the normal practice. `latest`, and tags that float within a major, are convenient locally and a source of "it worked yesterday" in deploys. The crash course's `node:19-alpine` is end of life. Use a current Node LTS Alpine tag, such as `node:24-alpine`.

---

## Part 5 — Pull, run, ports, and lifecycle

### Pull and run

**Q: How do you download an image without starting it?**
A: `docker pull nginx:1.23`. The client asks the default registry, downloads the layers, and `docker images` then shows the name, tag, and size. `docker pull nginx` downloads whatever `nginx:latest` points at.

**Q: How do you start a container?**
A: `docker run nginx:1.23` creates a new container and runs it in the foreground. Nginx logs stream in the terminal. Ctrl+C stops that container. `docker run` does not reuse a container you started earlier.

**Q: How do you keep the terminal?**
A: `docker run -d nginx:1.23`. **Detached** mode (`-d`) starts the container in the background and prints the full container id. `docker ps` shows a short id, the image, status, and a generated name. `docker logs <id-or-name>` prints the process output. Add `-f` to follow and `--tail 100` to limit it.

**Q: Do you have to pull before run?**
A: No. `docker run` looks locally, then pulls from the default registry if the tag is missing, then starts. `docker run -d nginx:1.22-alpine` is enough for an image you have never downloaded. That is how two Nginx versions run at once: two `docker run` commands, two tags, two containers.

### Port binding

**Q: Why is a running container unreachable in the browser?**
A: It sits on Docker's own network. The process listens on its port inside that network. Nothing on the host is connected to that port until you publish it. Nginx listens on 80, Redis on 6379, MySQL on 3306, the sample Node app on 3000. Those are container ports.

**Q: How do you publish a port?**
A: `-p host:container` on `docker run`. `docker run -d -p 9000:80 nginx:1.23` serves the container's port 80 at `http://localhost:9000`. The `PORTS` column of `docker ps` shows `0.0.0.0:9000->80/tcp`. Other containers should still use the container port, not the host port.

**Q: Which host port should you pick?**
A: The same number as the container port when it is free, such as `-p 3306:3306` for MySQL. Use another host port (`9000:80`) when the host port is taken or you are running two copies. Only one process on the host can bind a given port.

### Start, stop, and names

**Q: Why does `docker ps` hide containers you just stopped?**
A: `docker ps` lists running containers only. Stopped containers still exist, with status `Exited`. `docker ps -a` lists both. `docker run` created a new one each time, so several exited Nginx containers can pile up.

**Q: How do you stop and start without creating a new container?**
A: `docker stop <id-or-name>` sends SIGTERM, waits (10 seconds by default), then SIGKILL. `docker start <id-or-name>` runs that same container again, including its port publish and name. You can pass several names to one `stop` or `start`. `docker kill` skips the graceful signal.

**Q: How do you name a container?**
A: `docker run -d --name web-app -p 9000:80 nginx:1.23`. Without `--name`, Docker assigns a random name. Every later command accepts the name or the id: `docker logs web-app`, `docker stop web-app`. Names must be unique among existing containers, including stopped ones.

---

## Part 6 — Dockerfile

### Instructions

**Q: What is a Dockerfile?**
A: A text file named `Dockerfile` that defines how to build an image from your application. It lives at the root of the build context. Each instruction adds a layer. The file is the repeatable replacement for the old install guide.

**Q: What is a base image, and how do you select it?**
A: `FROM` sets the image you extend. It is usually a small Linux image that already has your runtime. A Node app uses a Node image, a Java app uses an image with a JRE. `node:24-alpine` means Node on **Alpine**, a small Linux distribution. Alpine uses musl, not glibc. If a native dependency fails there, switch to `node:24-slim`.

**Q: What do `COPY`, `WORKDIR`, `RUN`, and `CMD` do?**
A: `COPY` puts files from your machine into the image. The image filesystem is not your host. A trailing slash on the destination (`/app/`) makes Docker treat it as a directory and create it. `WORKDIR /app` is `cd` for every instruction after it. `RUN` executes at **build** time and saves the result in a layer (`npm ci`). `CMD` is the process started when the container runs, not during the build.

**Q: Why is the start command `CMD` and not `RUN`?**
A: `RUN` finishes during `docker build`. If you `RUN node server.js`, the build hangs on a server that never exits, or the process is not running when the container later starts. `CMD` is recorded and executed on `docker run`. Prefer the exec form, `CMD ["node", "server.js"]`, so Node is PID 1 and receives Ctrl+C. The shell form `CMD node server.js` wraps a shell and often swallows that signal.

**Q: What does a minimal Node Dockerfile look like?**
A: Copy the lockfile before the source so dependency installs stay cached when only code changes. `npm ci` installs exactly the lockfile.

```dockerfile
FROM node:24-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

The crash course order was `FROM node:19-alpine`, `COPY` of `package.json` and the source into `/app/`, `WORKDIR /app`, `RUN npm install`, then `CMD` of `node server.js`. Same five ideas. The file above adds cache order, a non-root user, and `EXPOSE`.

**Q: What does `EXPOSE` actually do?**
A: It documents the container port. It does not publish it. You still pass `-p 3000:3000`. Readers and Compose use `EXPOSE` as the intended port.

### Build and run

**Q: How do you build an image from a Dockerfile?**
A: From the directory that contains it: `docker build -t node-app:1.0 .`. `-t` sets `name:tag`. The final `.` is the **build context**, the files sent to the engine. The engine runs each instruction in order. `docker images` then lists `node-app` with tag `1.0`.

**Q: How do you run the image you just built?**
A: `docker run -d --name node-app -p 3000:3000 node-app:1.0`. The app listens on 3000 inside the container. The host port is the left side. `http://localhost:3000` hits it, and `docker logs node-app` shows the request. Anything you put after the image name replaces `CMD`.

**Q: What should stay out of the build context?**
A: A `.dockerignore` next to the Dockerfile. Ignore `node_modules`, `.git`, `.env`, logs, and local build output. `COPY . .` otherwise sends secrets into the image and can copy a host `node_modules` built for the wrong OS. The context is uploaded before the first instruction, so a huge folder makes every build slow even when layers cache.

---

## Part 7 — Development lifecycle

### From laptop to a dev server

**Q: Where does Docker sit while you are coding?**
A: You run the app's dependencies as containers from Hub instead of installing them on the laptop. A JavaScript app talks to a MongoDB container. You do not need MongoDB installed on the OS. Your own app can still run on the host during coding, or it can be a container too.

**Q: What happens after you commit?**
A: The commit triggers CI. CI builds the application, builds an image from the Dockerfile, and pushes that image to a **private** repository. A dev server pulls your image from that private repository and pulls MongoDB from Docker Hub. Both containers run on the server and are configured to reach each other. A tester uses the dev server, not your laptop.

**Q: What is the shape of that pipeline?**
A: (1) Develop against dependency containers. (2) Commit. (3) CI builds and tags the image, ideally with the commit id, not only `latest`. (4) Push to a private registry. (5) The environment pulls and runs your image plus public dependency images. (6) Configure them to talk, then point people at that environment. The same image moves to the next environment. You do not rebuild it with different contents per stage.

---

## Part 8 — Commands and practices you still need

### Cleanup, shell, and inspect

**Q: How do you delete containers and images?**
A: `docker rm web-app` removes a stopped container. `docker rm -f web-app` stops and removes it. `docker rmi node-app:1.0` removes an image that no container still references. `docker run --rm` deletes the container when it exits, which is right for one-off commands and wrong for a database you meant to keep.

**Q: How do you reclaim disk?**
A: `docker system df` shows images, containers, and volumes. `docker container prune` removes stopped containers. `docker image prune` removes dangling layers. `docker system prune` removes stopped containers, unused networks, and dangling images. Add `-a` to also drop unused images. Prune never deletes a volume unless you pass `--volumes`. Do not prune volumes until you know they are not data.

**Q: How do you open a shell inside a running container?**
A: `docker exec -it web-app sh`. `exec` starts another process in that container. Alpine images have `sh`, not `bash`. `-it` allocates a terminal. Exit the shell and the container keeps running. `docker inspect web-app` prints the full config: env, mounts, IP, and state.

### Data, config, and networks

**Q: Why does database data disappear?**
A: The container's writable layer is deleted with the container. Anything a database writes inside its own filesystem is gone after `docker rm`. A **named volume** keeps that directory on the host, managed by Docker: `docker run -d --name db -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:16`. `docker volume ls` lists volumes. Removing the container does not remove `pgdata`.

**Q: How do you pass configuration in?**
A: `-e KEY=value`, or `--env-file .env` so the file is not baked into the image. In the Dockerfile, `ENV NODE_ENV=production` sets a default. Do not `COPY` a secrets file. A secret in a layer stays in the image history after you delete the line.

**Q: How do two containers find each other?**
A: Put them on a user-defined network. Compose does this for you, and the service name is the DNS name. By hand: `docker network create appnet`, then `docker run -d --name db --network appnet postgres:16` and `docker run -d --name api --network appnet -e DATABASE_URL=postgres://db:5432/app node-app:1.0`. The app uses hostname `db` and the **container** port. The default bridge network does not resolve container names.

**Q: What restart policy should a long-running container use?**
A: `--restart unless-stopped` so a crash or a daemon reboot brings it back, and so a container you explicitly stopped stays stopped. `always` also restarts one you stopped, after the daemon restarts. `on-failure` restarts only on a non-zero exit. The default is `no`.

### Image habits that prevent the usual outages

**Q: How should layers be ordered?**
A: Put the things that change least first. `FROM`, then dependency files, then `RUN npm ci`, then `COPY` of the source. A source-only change reuses the install layer. `COPY . .` before `npm ci` reruns the install on every edit. Each instruction is a layer. `docker history node-app:1.0` shows them.

**Q: What belongs in one container?**
A: One main process. A web server and its database are two containers, not one image with both started by a shell script. The container's job is that process. Logs go to stdout so `docker logs` works, not only to a file inside the container.

**Q: Why run as a non-root user?**
A: A process that is root inside the container is a worse breakout if the app is compromised. Official Node images include a `node` user. `USER node` after `RUN npm ci` (which needs to write as root) drops privileges for `CMD`. Files copied earlier must be readable by that user.

**Q: When do you use a multi-stage build?**
A: When the build needs a compiler, a full SDK, or dev dependencies that the running app does not. The first stage builds. The final stage is a slim runtime image and `COPY --from=build` takes only the artifact. The published image stays smaller and has no toolchain in it.

### Compose

**Q: What problem does Compose solve?**
A: The crash course's "ten services, ten commands" still leaves you with a manual list of `docker run` flags. **Compose** is one file that defines the set, the network, the volumes, and the ports. The CLI is `docker compose` (a space). `docker-compose` with a hyphen is the old standalone binary.

**Q: What does a minimal Compose file look like?**
A: `compose.yaml` next to the Dockerfile. `docker compose up -d` builds and starts it. `docker compose logs -f app` follows logs. `docker compose down` removes the containers and the network. `docker compose down -v` also deletes the named volume.

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      MONGO_URL: mongodb://mongo:27017/app
    depends_on:
      - mongo
  mongo:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
volumes:
  mongo-data:
```

`depends_on` waits until the dependency container has started, not until the database is ready to accept queries. The app still needs to retry its first connection. The hostname is the service name, `mongo`.

### Publish

**Q: How do you push an image to a registry?**
A: `docker login` (or the cloud CLI's registry login) stores credentials for that host. Tag the image with the full repository name, then push that tag. Hub's short name `node-app:1.0` is really `docker.io/<user>/node-app:1.0` once you set the namespace.

```bash
docker tag node-app:1.0 registry.example.com/team/node-app:1.0
docker push registry.example.com/team/node-app:1.0
```

**Q: How should the tag be chosen in CI?**
A: Tag with the commit SHA so the environment can roll back to an immutable name. You may also move a floating tag such as `1.4` or `latest`, but the deploy command should pin the SHA. Do not push from a laptop as the normal release path. The pipeline that built the image is the thing that pushes it.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Image | Read-only package: app, runtime, and environment |
| Container | Running instance of an image |
| Layer | One Dockerfile instruction, cached and reused |
| Registry | Service that stores image repositories |
| Repository | One application's images inside a registry |
| Tag | Version label on an image, `name:tag` |
| `latest` | Default tag when you omit one; just a label |
| Base image | The `FROM` image you add your app on top of |
| Build context | Directory sent to the engine, the final `docker build` argument |
| Publish | `-p host:container` maps a host port to a container port |
| Volume | Named storage that outlives the container |
| Engine | Daemon that builds images and runs containers |
| Docker Desktop | Engine plus CLI plus GUI, with a Linux VM on Mac and Windows |
| Official image | Hub image reviewed with the vendor and security practices |
| Detached | `-d`, container in the background, id printed |
| `CMD` | Process started on `docker run` |
| `RUN` | Command executed at build time and saved as a layer |
| `EXPOSE` | Documents the container port; does not publish it |
| Compose | One file that runs a set of containers together |
| OCI | The image and runtime standard Docker implements |

---

## Formulas

- **Pull:** `docker pull name:tag`
- **Run:** `docker run -d --name app -p 3000:3000 --restart unless-stopped name:tag`
- **Run and remove:** `docker run --rm -it name:tag sh`
- **Logs:** `docker logs -f --tail 100 app`
- **Lifecycle:** `docker ps -a` · `docker stop app` · `docker start app` · `docker rm -f app`
- **Shell:** `docker exec -it app sh`
- **Build:** `docker build -t name:tag .`
- **Disk:** `docker system df` · `docker system prune`
- **Volume:** `docker run -d -v data:/path/in/container name:tag`
- **Network:** `docker network create appnet` then `--network appnet`, hostname = container name
- **Env:** `docker run -e KEY=value` or `--env-file .env`
- **Publish:** `docker tag name:tag host/namespace/name:tag` then `docker push host/namespace/name:tag`
- **Compose:** `docker compose up -d` · `docker compose logs -f` · `docker compose down`
- **Port map:** `-p <host>:<container>`
- **Start process:** `CMD ["executable", "arg"]`

---

*Study aid. The crash course is TechWorld with Nana's Docker Crash Course for Absolute Beginners (https://www.youtube.com/watch?v=pg19Z8LL06w). For current install steps, Dockerfile reference, and Compose, use the official Docker documentation.*
