# VM Snapshot Reverter

A web application that helps manage and revert VMware ESXi virtual machines to their latest snapshots. The application provides a simple web interface to connect to an ESXi host and execute snapshot reversion operations.

## Features

- Web-based interface for ESXi host management
- Secure SSH connection to ESXi hosts
- Automatic detection of VMs and their snapshot status
- Support for both persistent and non-persistent disk modes
- Batch operations for multiple VMs

## Prerequisites

- Docker and Docker Compose
- ESXi host with SSH access enabled
- Valid credentials for the ESXi host

## Quick Start

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd revert-vm-image
   ```

2. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

4. Enter your ESXi host details and click "Execute" to manage VM snapshots.

## How It Works

The application performs the following operations:

1. Connects to the specified ESXi host via SSH
2. Identifies all VMs and their snapshot status
3. For each VM, it will:
   - Revert to the latest snapshot if one exists and the disk is persistent
   - Power cycle the VM if no snapshot exists and the disk is non-persistent

## Security Notes

- The application requires SSH access to your ESXi host
- Credentials are transmitted securely over the network
- No credentials are stored persistently
- Ensure your ESXi host's firewall allows SSH connections from the application server

## Troubleshooting

- **Connection Issues**: Verify that SSH is enabled on your ESXi host and the credentials are correct
- **Permission Errors**: Ensure the provided user has sufficient privileges to manage VMs and snapshots
- **Script Execution**: Check the application logs for detailed error messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
