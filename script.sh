#!/bin/sh

# Get all VMs with proper parsing to handle multi-word names
vim-cmd vmsvc/getallvms | awk 'NR>1 {print $1 "\t" $2}' | while IFS=$'\t' read vmid name; do
  # Skip if vmid is not numeric
  if ! echo "$vmid" | grep -q '^[0-9]\+$'; then
    continue
  fi

  # Get latest snapshot ID
  snapid=$(vim-cmd vmsvc/snapshot.get $vmid 2>/dev/null | grep "Snapshot Id" | tail -1 | awk -F': ' '{print $2}' | xargs)

  # Get disk mode
  mode=$(vim-cmd vmsvc/device.getdevices $vmid 2>/dev/null | grep diskMode | awk -F'"' '{print $2}' | sort -u | tail -1)

  # Case 1: Snapshot exists + persistent
  if [ -n "$snapid" ] && [ "$snapid" != "null" ] && [ "$mode" = "persistent" ]; then
    echo "# $vmid $name"
    echo "vim-cmd vmsvc/snapshot.revert $vmid $snapid 0 &"
    echo "sleep 10"
    echo "vim-cmd vmsvc/power.on $vmid"
    echo "sleep 5"
    echo

  # Case 2: No snapshot + nonpersistent → power cycle
  elif [ -z "$snapid" ] && echo "$mode" | grep -q "independent_nonpersistent"; then
    echo "# $vmid $name"
    echo "vim-cmd vmsvc/power.off $vmid"
    echo "sleep 10"
    echo "vim-cmd vmsvc/power.on $vmid"
    echo "sleep 5"
    echo
  fi
done
