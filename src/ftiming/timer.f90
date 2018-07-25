!
! Author: Rongyang Sun <sun-rongyang@outlook.com>
! Creation Date: 2018-05-22
! 
! Description: zzdmrg-fortran project. A Timer class.
!


module Timer_class
  implicit none
  integer, parameter :: kP14 = selected_real_kind(p=14)

  type, public :: Timer
    private
    real(kind=kP14) :: saved_time
  contains
    procedure, public :: start_timer => start_timer_sub
    procedure, public :: elapsed_time => elapsed_time_fn
    procedure, public :: print_elap_time => print_elap_time_sub
  end type Timer

  private :: start_timer_sub, elapsed_time_fn, print_elap_time_sub
  contains
    subroutine start_timer_sub(this)
      implicit none
      class(Timer) :: this
      integer, dimension(8) :: value

      call date_and_time(values=value)
      this%saved_time = 86400.d0 * value(3) + 3600.d0 * value(5) &
                  + 60.d0 * value(6) + value(7) + 0.001d0 * value(8)
    end subroutine start_timer_sub

    real function elapsed_time_fn(this)
      implicit none
      class(Timer) :: this
      integer, dimension(8) :: value
      real(kind=kP14) :: current_time

      call date_and_time(values=value)
      current_time = 86400.d0 * value(3) + 3600.d0 * value(5) &
                + 60.d0 * value(6) + value(7) + 0.001d0 * value(8)
      elapsed_time_fn = current_time - this%saved_time
    end function elapsed_time_fn

    subroutine print_elap_time_sub(this, mark_text)
      implicit none
      class(Timer) :: this
      character(len=*) :: mark_text
      real(kind=kP14) :: elap_time

      elap_time = this%elapsed_time()
      write(*,1000) "[timing]", mark_text, elap_time
      1000 format(A8, 1X, A32, 1X, F15.3)
    end subroutine print_elap_time_sub
end module Timer_class
