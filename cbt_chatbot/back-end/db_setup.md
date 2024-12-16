# Database Setup Instructions

Follow these steps to set up the PostgreSQL database using Docker:

1. **Download Docker**: [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Open Docker Terminal**: Launch the Docker terminal to run the following commands.

3. **Pull PostgreSQL Image**:
    ```sh
    docker pull postgres
    ```

4. **Create Docker Volume**:
    ```sh
    docker volume create postgres_data
    ```

5. **Run PostgreSQL Container**:
    ```sh
    docker run --name postgres_container -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
    ```

**Credentials**:
- **Username**: `postgres`
- **Password**: `mysecretpassword`
