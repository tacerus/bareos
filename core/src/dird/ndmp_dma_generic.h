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

#ifndef DIRD_NDMP_DMA_GENERIC_H_
#define DIRD_NDMP_DMA_GENERIC_H_

bool ndmp_validate_client(JobControlRecord *jcr);
bool ndmp_validate_storage(JobControlRecord *jcr);
void do_ndmp_client_status(UaContext *ua, ClientResource *client, char *cmd);

#endif // DIRD_NDMP_DMA_GENERIC_H_
