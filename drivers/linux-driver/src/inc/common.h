/*
 *    RoboPeak USB LCD Display Linux Driver
 *    
 *    Copyright (C) 2009 - 2013 RoboPeak Team
 *    This file is licensed under the GPL. See LICENSE in the package.
 *
 *    http://www.robopeak.net
 *
 *    Author Shikai Chen
 *
 *  ----------------------------------------------------------------------
 *    Common Includes
 *
 */

#ifndef _COMMON_INCLUDE_H
#define _COMMON_INCLUDE_H

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/mutex.h>
#include <asm/uaccess.h>
#include <linux/usb.h>
#include <linux/list.h>
#include <linux/kthread.h> 
#include <linux/platform_device.h>
#include <linux/string.h>
#include <linux/delay.h>
#include <linux/fb.h>
#include <linux/mm.h>
#include <linux/vmalloc.h>
#include <linux/input.h>
#include <linux/wait.h>

#include "inc/types.h"
#include "inc/drvconf.h"
#include "inc/devconf.h"


#include "inc/protocol.h"

extern int fps;
#define RPUSBDISP_STATUS_BUFFER_SIZE   32


// object predefine
struct rpusbdisp_disp_ticket_bundle {
    int  ticket_count;
    struct list_head   ticket_list;

};

struct rpusbdisp_disp_ticket {
    struct urb                      *  transfer_urb;
    struct list_head                   ticket_list_node;
    struct rpusbdisp_dev            *  binded_dev;
    
};

struct rpusbdisp_disp_ticket_pool {
    struct list_head                   list;
    spinlock_t                         oplock;
    size_t                             disp_urb_count;
    size_t                             packet_size_factor;
    int                                availiable_count;
    wait_queue_head_t                  wait_queue;
    struct delayed_work                completion_work;

};  

struct rpusbdisp_dev {
    // timing and sync 
    struct list_head                   dev_list_node;
    int                                dev_id;
    struct mutex                       op_locker;
    __u8                               is_alive;

    // usb device info
    struct usb_device               *  udev;
    struct usb_interface            *  interface;
    

    // status package related
    __u8                               status_in_buffer[RPUSBDISP_STATUS_BUFFER_SIZE]; // data buffer for the status IN endpoint
    size_t                             status_in_buffer_recvsize;

        

    __u8                               status_in_ep_addr;
    wait_queue_head_t                  status_wait_queue;
    struct urb                      *  urb_status_query;
    int                                urb_status_fail_count;


    // display data related
    __u8                               disp_out_ep_addr;
    size_t                             disp_out_ep_max_size;

    struct rpusbdisp_disp_ticket_pool  disp_tickets_pool;



    void                            *  fb_handle;
    void                            *  touch_handle;

    __u16                              device_fwver;

    struct fb_info                   * usb_fb;
};

#ifndef err
#define err(format,arg...) printk(KERN_ERR format, ## arg)
#endif

#ifndef info
#define info(format,arg...) printk(KERN_ERR format, ## arg)
#endif


#endif


