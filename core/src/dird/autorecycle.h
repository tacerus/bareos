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

#ifndef DIRD_AUTORECYCLE_H_
#define DIRD_AUTORECYCLE_H_

bool find_recycled_volume(JobControlRecord *jcr, bool InChanger, MediaDbRecord *mr,
                          StoreResource *store, const char *unwanted_volumes);
bool recycle_oldest_purged_volume(JobControlRecord *jcr, bool InChanger, MediaDbRecord *mr,
                                  StoreResource *store, const char *unwanted_volumes);
bool recycle_volume(JobControlRecord *jcr, MediaDbRecord *mr);

#endif // DIRD_AUTORECYCLE_H_
