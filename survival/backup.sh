#!/bin/bash
# SURVIVAL MODE — Backup Script
# Run every 6 hours via cron
# Backup critical state files

SURVIVAL_DIR="/app/working/workspaces/default/survival"
BACKUP_DIR="$SURVIVAL_DIR/backup"
LOG_FILE="$SURVIVAL_DIR/logs/backup.log"

mkdir -p "$BACKUP_DIR"
mkdir -p "$SURVIVAL_DIR/logs"

timestamp=$(date +%Y%m%d_%H%M%S)

echo "[$(date)] Backup started" >> "$LOG_FILE"

# Backup state files
cp "$SURVIVAL_DIR/state.json" "$BACKUP_DIR/state_$timestamp.json" 2>/dev/null
cp "/app/working/workspaces/default/data/idx_action_state.json" "$BACKUP_DIR/idx_state_$timestamp.json" 2>/dev/null

# Keep only last 14 backups
ls -t "$BACKUP_DIR"/state_*.json 2>/dev/null | tail -n +15 | xargs rm -f 2>/dev/null
ls -t "$BACKUP_DIR"/idx_state_*.json 2>/dev/null | tail -n +15 | xargs rm -f 2>/dev/null

echo "[$(date)] Backup complete — $BACKUP_DIR" >> "$LOG_FILE"