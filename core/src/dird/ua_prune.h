/*
   BAREOS® - Backup Archiving REcovery Open Sourced

   Copyright (C) 2018-2018 Bareos GmbH & Co. KG

   This program is Free Software; you can redistribute it and/or
   modify it under the terms of version three of the GNU Affero General Public
   License as published by the Free Software Foundation and included
   in the file LICENSE.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301, USA.
*/

#ifndef DIRD_UA_PRUNE_H
#define DIRD_UA_PRUNE_H

#include "dird/ua.h"

bool prune_files(UaContext *ua, ClientResource *client, PoolResource *pool);
bool prune_jobs(UaContext *ua, ClientResource *client, PoolResource *pool, int JobType);
bool prune_volume(UaContext *ua, MediaDbRecord *mr);
int job_delete_handler(void *ctx, int num_fields, char **row);
int del_count_handler(void *ctx, int num_fields, char **row);
int file_delete_handler(void *ctx, int num_fields, char **row);
int get_prune_list_for_volume(UaContext *ua, MediaDbRecord *mr, del_ctx *del);
int exclude_running_jobs_from_list(del_ctx *prune_list);

#endif // DIRD_UA_PRUNE_H
